# Copyright (C) 2015-2018 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the Eclipse Public License v1.0 which
# accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
# Annika Wollschlaeger <annika.wollschlaeger@dlr.de>
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Lukas Becker <lukas.becker@dlr.de>
# Matthias Buettner <matthias.buettner@dlr.de>
# Rico Belder <rico.belder@dlr.de>
# Sebastian Brunner <sebastian.brunner@dlr.de>

"""
.. module:: library_tree
   :synopsis: The module holds controller tree overview of all mounted libraries and access to general
     functionality to add element or templates of those to a state-machine.

"""

import gobject
import gtk
import os
from functools import partial

from rafcon.core.states.library_state import LibraryState
from rafcon.gui.config import global_gui_config
from rafcon.gui.runtime_config import global_runtime_config
from rafcon.gui.controllers.utils.extended_controller import ExtendedController
from rafcon.gui.models.library_manager import LibraryManagerModel
from rafcon.gui.helpers.label import create_image_menu_item, append_sub_menu_to_parent_menu
from rafcon.gui.helpers.text_formatting import format_folder_name_human_readable
import rafcon.gui.singleton as gui_singletons
from rafcon.gui.utils import constants
from rafcon.gui.utils.dialog import RAFCONButtonDialog
from rafcon.utils import log

logger = log.get_logger(__name__)


class LibraryTreeController(ExtendedController):

    ID_STORAGE_ID = 0
    ITEM_STORAGE_ID = 1
    LIB_PATH_STORAGE_ID = 2
    OS_PATH_STORAGE_ID = 3
    TOOL_TIP_STORAGE_ID = 3
    LIB_KEY_STORAGE_ID = 4

    def __init__(self, model, view):
        assert isinstance(model, LibraryManagerModel)
        assert isinstance(view, gtk.TreeView)
        ExtendedController.__init__(self, model, view)
        self.tree_store = gtk.TreeStore(str, gobject.TYPE_PYOBJECT, str, str, str)
        view.set_model(self.tree_store)
        view.set_tooltip_column(3)

        view.drag_source_set(gtk.gdk.BUTTON1_MASK, [('STRING', 0, 0)], gtk.gdk.ACTION_COPY)

        self.library_row_iter_dict_by_library_path = {}
        self.__expansion_state = None

        self.update()

    def register_view(self, view):
        super(LibraryTreeController, self).register_view(view)
        self.view.connect('button_press_event', self.mouse_click)

        self.view.connect("drag-data-get", self.on_drag_data_get)
        self.view.connect("drag-begin", self.on_drag_begin)

    def generate_right_click_menu(self, kind='library'):
        menu = gtk.Menu()
        if kind == 'library':
            menu.append(create_image_menu_item("Add as library (link)", constants.BUTTON_ADD,
                                               partial(self.insert_button_clicked, as_template=False)))
            menu.append(create_image_menu_item("Add as template (copy)", constants.BUTTON_COPY,
                                               partial(self.insert_button_clicked, as_template=True)))
            menu.append(gtk.SeparatorMenuItem())
            menu.append(create_image_menu_item("Open", constants.BUTTON_OPEN, self.open_button_clicked))
            menu.append(create_image_menu_item("Open and run", constants.BUTTON_START, self.open_run_button_clicked))
            menu.append(gtk.SeparatorMenuItem())
            menu.append(create_image_menu_item("Remove library", constants.BUTTON_DEL, self.delete_button_clicked))

            sub_menu_item, sub_menu = append_sub_menu_to_parent_menu("Substitute as library", menu,
                                                                     constants.BUTTON_REFR)

            sub_menu.append(create_image_menu_item("Keep state name", constants.BUTTON_LEFTA,
                            partial(self.substitute_as_library_clicked, keep_name=True)))
            sub_menu.append(create_image_menu_item("Take name from Library", constants.BUTTON_EXCHANGE,
                            partial(self.substitute_as_library_clicked, keep_name=False)))

            sub_menu_item, sub_menu = append_sub_menu_to_parent_menu("Substitute as template", menu,
                                                                     constants.BUTTON_REFR)

            sub_menu.append(create_image_menu_item("Keep state name", constants.BUTTON_LEFTA,
                            partial(self.substitute_as_template_clicked, keep_name=True)))
            sub_menu.append(create_image_menu_item("Take name from Library", constants.BUTTON_EXCHANGE,
                            partial(self.substitute_as_template_clicked, keep_name=False)))
        elif kind == 'library root':
            menu.append(create_image_menu_item("Add library root", constants.BUTTON_DEL, self.add_button_clicked))
            menu.append(create_image_menu_item("Remove library root", constants.BUTTON_DEL, self.delete_button_clicked))
        elif kind == 'libraries':
            menu.append(create_image_menu_item("Remove libraries", constants.BUTTON_DEL, self.delete_button_clicked))
        elif kind == 'library tree':
            menu.append(create_image_menu_item("Add library root", constants.BUTTON_DEL, self.add_button_clicked))

        return menu

    def mouse_click(self, widget, event=None):
        # Double click with left mouse button
        if event.type == gtk.gdk._2BUTTON_PRESS and event.button == 1:
            (model, row) = self.view.get_selection().get_selected()
            if isinstance(model[row][self.ITEM_STORAGE_ID], dict):  # double click on folder, not library
                state_row_path = self.tree_store.get_path(row)
                if state_row_path is not None:
                    if self.view.row_expanded(state_row_path):
                        self.view.collapse_row(state_row_path)
                    else:
                        self.view.expand_to_path(state_row_path)
                return False
            self.open_button_clicked(None)
            return True

        # Single right click
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:

            x = int(event.x)
            y = int(event.y)
            time = event.time
            pthinfo = self.view.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                self.view.grab_focus()
                self.view.set_cursor(path, col, 0)

                (model, row) = self.view.get_selection().get_selected()
                if isinstance(model[row][self.ITEM_STORAGE_ID], dict):  # right click on folder, not library
                    if model[row][self.LIB_PATH_STORAGE_ID] == '':
                        menu = self.generate_right_click_menu('library root')
                    else:
                        menu = self.generate_right_click_menu('libraries')
                else:
                    menu = self.generate_right_click_menu('library')
            else:
                menu = self.generate_right_click_menu('library tree')
            menu.show_all()
            menu.popup(None, None, None, event.button, time)
            return True

    @ExtendedController.observe("library_manager", after=True)
    def model_changed(self, model, prop_name, info):
        self.update()

    def store_expansion_state(self):
        # print "\n\n store of state machine {0} \n\n".format(self.__my_selected_sm_id)
        try:
            act_expansion_library = {}
            for library_path, library_row_iter in self.library_row_iter_dict_by_library_path.iteritems():
                library_row_path = self.tree_store.get_path(library_row_iter)
                act_expansion_library[library_path] = self.view.row_expanded(library_row_path)
                # if act_expansion_library[library_path]:
                #     print library_path
            self.__expansion_state = act_expansion_library
        except TypeError:
            logger.warn("expansion state of library could not be stored")

    def redo_expansion_state(self):
        if self.__expansion_state:
            # print "\n\n redo of state machine {0} \n\n".format(self.__my_selected_sm_id)
            try:
                for library_path, library_row_expanded in self.__expansion_state.iteritems():
                    library_row_iter = self.library_row_iter_dict_by_library_path[library_path]
                    if library_row_iter:  # may elements are missing afterwards
                        library_row_path = self.tree_store.get_path(library_row_iter)
                        if library_row_expanded:
                            self.view.expand_to_path(library_row_path)
                            # print library_path
            except (TypeError, KeyError):
                logger.warn("expansion state of library tree could not be re-done")

    def update(self):
        self.store_expansion_state()
        self.tree_store.clear()
        self.library_row_iter_dict_by_library_path.clear()
        for library_key, library_item in self.model.library_manager.libraries.iteritems():
            self.insert_rec(None, library_key, library_item, "")
        self.redo_expansion_state()
        if self.__expansion_state:
            logger.info("Libraries have been updated")
        else:
            logger.info("Library tree has been initialized")

    @staticmethod
    def convert_if_human_readable(s):
        """Converts a string to format which is more human readable"""
        return format_folder_name_human_readable(s) \
            if global_gui_config.get_config_value('LIBRARY_TREE_PATH_HUMAN_READABLE', False) else s

    def insert_rec(self, parent, library_key, library_item, library_path, library_root_path=None):
        """

        :param parent:
        :param str library_key:
        :param library_item:
        :param str library_path:
        :param str library_root_path:
        :return:
        """
        _library_key = self.convert_if_human_readable(library_key)
        tool_tip = library_item if isinstance(library_item, str) else ''
        if not tool_tip and parent is None:
            library_root_path = tool_tip = self.model.library_manager._library_root_paths.get(library_key, '')
        if not tool_tip:
            partial_path = ''
            if len(library_path.split(os.path.sep)) > 1:
                partial_path = os.path.sep.join(library_path.split(os.path.sep)[1:])
            tool_tip = os.path.join(library_root_path, partial_path, library_key)
        tree_item = self.tree_store.insert_before(parent, None, (_library_key, library_item, library_path,
                                                                 tool_tip, library_key))
        if isinstance(library_item, dict) and not library_item:
            return
        if not library_path:
            library_path = library_key
        else:
            library_path = os.path.join(library_path, library_key)
        self.library_row_iter_dict_by_library_path[library_path] = tree_item
        if isinstance(library_item, dict):
            for child_library_key, child_library_item in library_item.iteritems():
                self.insert_rec(tree_item, child_library_key, child_library_item, library_path, library_root_path)

    def on_drag_data_get(self, widget, context, data, info, time):
        """dragged state is inserted and its state_id sent to the receiver

        :param widget:
        :param context:
        :param data: SelectionData: contains state_id
        :param info:
        :param time:
        """
        library_state = self._get_selected_library_state()
        import rafcon.gui.helpers.state_machine as gui_helper_state_machine
        gui_helper_state_machine.add_state_by_drag_and_drop(library_state, data)

    def on_drag_begin(self, widget, context):
        """replace drag icon

        :param widget:
        :param context:
        """
        self.view.drag_source_set_icon_stock(gtk.STOCK_NEW)

    def insert_button_clicked(self, widget, as_template=False):
        import rafcon.gui.helpers.state_machine as gui_helper_state_machine
        gui_helper_state_machine.insert_state_into_selected_state(self._get_selected_library_state(), as_template)

    def select_open_state_machine_of_selected_library_element(self):
        """Select respective state machine of selected library in state machine manager if already open """
        (model, row_path) = self.view.get_selection().get_selected()
        if row_path:
            physical_library_path = model[row_path][self.ITEM_STORAGE_ID]
            smm = gui_singletons.state_machine_manager_model.state_machine_manager
            sm = smm.get_open_state_machine_of_file_system_path(physical_library_path)
            if sm:
                gui_singletons.state_machine_manager_model.selected_state_machine_id = sm.state_machine_id

    def open_button_clicked(self, widget):
        try:
            self.open_library_as_state_machine()
        except (AttributeError, ValueError) as e:
            logger.error("Could not open library: {0}".format(e))

    def open_run_button_clicked(self, widget):
        from rafcon.core.singleton import state_machine_execution_engine
        state_machine = self.open_library_as_state_machine()
        state_machine_execution_engine.start(state_machine.state_machine_id)

    def open_library_as_state_machine(self):
        import rafcon.gui.helpers.state_machine as gui_helper_state_machine
        (model, row) = self.view.get_selection().get_selected()
        physical_library_path = model[row][self.ITEM_STORAGE_ID]
        assert isinstance(physical_library_path, str)

        logger.debug("Opening library as state-machine from path '{0}'".format(physical_library_path))
        state_machine = gui_helper_state_machine.open_state_machine(physical_library_path)
        global_runtime_config.update_recently_opened_state_machines_with(state_machine)
        return state_machine

    def add_button_clicked(self, widget):
        if "library root" in widget.get_label():
            logger.info("Get new path and mounting key.")
            from rafcon.gui import interface
            from rafcon.gui.singleton import global_config, global_runtime_config

            _path = interface.save_folder("Please choose the folder to be mounted and insert your mounting key.",
                                          "insert your mounting key here")

            if _path is None:
                return
            path_elements = _path.split(os.path.sep)
            library_root_key = path_elements[-1]  # the file/folder name is the mounting key
            library_root_path = os.path.sep.join(path_elements[:-1])

            logger.info("Add new library root '{0}: {1}' to config.".format(library_root_key, library_root_path))
            library_paths = global_config.get_config_value('LIBRARY_PATHS')
            library_paths[library_root_key] = library_root_path
            global_config.save_configuration()
            self.model.library_manager.refresh_libraries()

    def delete_button_clicked(self, widget):
        """Removes library from hard drive after request second confirmation"""
        logger.info("delete library" + str(widget) + str(widget.get_label()))
        model, path = self.view.get_selection().get_selected()
        if path:
            # Second confirmation to delete library
            tree_m_row = self.tree_store[path]
            # assert isinstance(tree_m_row[self.ITEM_STORAGE_ID], str)
            library_file_system_path = tree_m_row[self.OS_PATH_STORAGE_ID]

            if "root" in widget.get_label():
                button_texts = [widget.get_label() + "from tree and config", "Cancel"]
                partial_message = "This will remove the library root from your configuration (config.yaml)."
            else:
                button_texts = [widget.get_label(), "Cancel"]
                partial_message = "This folder will be removed from hard drive! You really wanna do that?"

            message_string = "You choose to {2} with " \
                             "\n\nlibrary tree path:   {0}" \
                             "\n\nphysical path:        {1}.\n\n\n"\
                             "{3}" \
                             "".format(os.path.join(self.convert_if_human_readable(tree_m_row[self.LIB_PATH_STORAGE_ID]),
                                                    tree_m_row[self.ID_STORAGE_ID]),
                                       library_file_system_path,
                                       widget.get_label().lower(),
                                       partial_message)

            width = 8*len("physical path:        " + library_file_system_path)
            dialog = RAFCONButtonDialog(message_string, button_texts, message_type=gtk.MESSAGE_QUESTION,
                                        parent=self.get_root_window(), width=min(width, 1400))
            response_id = dialog.run()
            dialog.destroy()
            if response_id == 1:
                if "root" in widget.get_label():
                    logger.info("Remove library root key '{0}' from config.".format(tree_m_row[self.ID_STORAGE_ID]))
                    from rafcon.gui.singleton import global_config
                    library_paths = global_config.get_config_value('LIBRARY_PATHS')
                    del library_paths[tree_m_row[self.LIB_KEY_STORAGE_ID]]
                    global_config.save_configuration()
                    self.model.library_manager.refresh_libraries()
                elif "libraries" in widget.get_label():
                    logger.debug("Remove of all libraries in {} is triggered.".format(tree_m_row[self.OS_PATH_STORAGE_ID]))
                    import shutil
                    shutil.rmtree(tree_m_row[self.OS_PATH_STORAGE_ID])
                    self.model.library_manager.refresh_libraries()
                else:
                    logger.debug("Remove of Library {} is triggered.".format(tree_m_row[self.ITEM_STORAGE_ID]))
                    self.model.library_manager.remove_library_from_file_system(tree_m_row[self.LIB_PATH_STORAGE_ID],
                                                                               tree_m_row[self.ID_STORAGE_ID])
            elif response_id in [2, -4]:
                pass
            else:
                logger.warning("Response id: {} is not considered".format(response_id))

            return True
        return False

    def substitute_as_library_clicked(self, widget, keep_name=True):
        import rafcon.gui.helpers.state_machine as gui_helper_state_machine
        gui_helper_state_machine.substitute_selected_state(self._get_selected_library_state(), as_template=False,
                                                           keep_name=keep_name)

    def substitute_as_template_clicked(self, widget, keep_name=True):
        import rafcon.gui.helpers.state_machine as gui_helper_state_machine
        gui_helper_state_machine.substitute_selected_state(self._get_selected_library_state(), as_template=True,
                                                           keep_name=keep_name)

    def _get_selected_library_state(self):
        """Returns the LibraryState which was selected in the LibraryTree

        :return: selected state in TreeView
        :rtype: LibraryState
        """
        (model, row) = self.view.get_selection().get_selected()
        library_item_key = model[row][self.ID_STORAGE_ID]
        library_item = model[row][self.ITEM_STORAGE_ID]
        library_path = model[row][self.LIB_PATH_STORAGE_ID]

        if isinstance(library_item, dict):
            return None
        assert isinstance(library_item, str)
        library_file_system_path = library_item

        logger.debug("Link library state '{0}' (with library tree path: {2} and file system path: {1}) into state "
                     "machine.".format(str(library_item_key), library_file_system_path,
                                       self.convert_if_human_readable(str(library_path)) + "/" + str(library_item_key)))
        library_name = library_file_system_path.split(os.path.sep)[-1]
        return LibraryState(library_path, library_name, "0.1", format_folder_name_human_readable(library_name))
