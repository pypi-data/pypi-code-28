from django import VERSION as django_version
import datetime
import random
import string

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

import aristotle_mdr.models as models
import aristotle_mdr.perms as perms
from aristotle_mdr.utils import url_slugify_concept

from django_tools.unittest_utils.BrowserDebug import debug_response

from time import sleep


def wait_for_signal_to_fire(seconds=1):
    sleep(seconds)


def model_to_dict(item):
    from django.forms import model_to_dict as mtd
    return dict((k, v) for (k, v) in mtd(item).items() if v is not None)


def get_management_forms(item, slots=False, identifiers=False, item_is_model=False):

    d = {}

    if slots:
        d['slots-TOTAL_FORMS'] = 0
        d['slots-INITIAL_FORMS'] = 0
        d['slots-MIN_NUM_FORMS'] = 0
        d['slots-MAX_NUM_FORMS'] = 0

    if identifiers:
        d['identifiers-TOTAL_FORMS'] = 0
        d['identifiers-INITIAL_FORMS'] = 0
        d['identifiers-MIN_NUM_FORMS'] = 0
        d['identifiers-MAX_NUM_FORMS'] = 1

    if hasattr(item, 'serialize_weak_entities'):
        weak = item.serialize_weak_entities
        for entity in weak:
            d['%s-TOTAL_FORMS'%entity[0]] = 0
            d['%s-INITIAL_FORMS'%entity[0]] = 0
            d['%s-MIN_NUM_FORMS'%entity[0]] = 0
            d['%s-MAX_NUM_FORMS'%entity[0]] = 1000

    add_through_forms = False
    if not item_is_model:
        if isinstance(item, models.DataElementDerivation):
            add_through_forms = True
    else:
        if issubclass(item, models.DataElementDerivation):
            add_through_forms = True

    if add_through_forms:
        prefixes = ['derives', 'inputs']
        for pre in prefixes:
            d['%s-TOTAL_FORMS'%pre] = 0
            d['%s-INITIAL_FORMS'%pre] = 0
            d['%s-MIN_NUM_FORMS'%pre] = 0
            d['%s-MAX_NUM_FORMS'%pre] = 1000

    return d


def get_admin_management_forms(item_class):

    d = {}
    if issubclass(item_class, models.DataElementDerivation):
        prefixes = ['dedderivesthrough_set', 'dedinputsthrough_set']
        for pre in prefixes:
            d['%s-TOTAL_FORMS'%pre] = 0
            d['%s-INITIAL_FORMS'%pre] = 0
            d['%s-MIN_NUM_FORMS'%pre] = 0
            d['%s-MAX_NUM_FORMS'%pre] = 1000

    return d


def model_to_dict_with_change_time(item, fetch_time=None):
    """
    This constructs a dictionary from a model, with a last_fetched value as well
    that is needed for checking in edit forms to prevent overrides of other saves.
    """
    if fetch_time is None:
        fetch_time = timezone.now()
    d = model_to_dict(item)
    d['last_fetched'] = str(fetch_time)

    mfs = get_management_forms(item, slots=True, identifiers=True)
    d.update(mfs)

    return d


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_json_from_response(response):
    return response.json()


# Since all managed objects have the same rules, these can be used to cover everything
# This isn't an actual TestCase, we'll just pretend it is
class ManagedObjectVisibility(object):
    def setUp(self):
        self.ra = models.RegistrationAuthority.objects.create(
            name="Test RA",
            definition="My RA",
            public_state=models.STATES.qualified,
            locked_state=models.STATES.candidate
        )

        self.wg = models.Workgroup.objects.create(name="Test WG", definition="My WG")
        #RAFIX self.wg.registrationAuthorities.add(self.ra)

    def test_object_is_public(self):
        self.assertEqual(self.item.is_public(), False)
        s = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=models.STATES.notprogressed
        )
        self.assertEqual(self.item.is_public(), False)

        s.state = self.ra.public_state
        s.save()

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), True)

        s.state = self.ra.locked_state
        s.save()

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), False)

    def test_object_visibility_over_time(self):
        date = datetime.date
        s1 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2000, 1, 1),
            state=models.STATES.incomplete,
            changeDetails="s1",
        )

        # Overlaps s1 (it has no end)
        s2 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2005, 1, 1),
            until_date=datetime.date(2005, 6, 29),
            state=self.ra.public_state,
            changeDetails="s2",
        )

        # Deliberately miss 2005-06-30
        # Overlaps s1 (no end)
        s3 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2005, 7, 1),
            state=self.ra.public_state,
            changeDetails="s3",
        )

        # Overlaps s1 and s3 (no end)
        s4 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2006, 1, 1),
            until_date=datetime.date(2006, 12, 30),
            state=self.ra.locked_state,
            changeDetails="s4",
        )

        # Overlaps s1 and s3 (no end), completely contanied within s4
        s5 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2006, 3, 1),
            until_date=datetime.date(2006, 7, 30),
            state=self.ra.public_state,
            changeDetails="s5",
        )

        # Overlaps s1 and s3 (no end), overlaps s4 in 2006-11
        s6 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=datetime.date(2006, 11, 1),
            until_date=datetime.date(2008, 7, 30),
            state=self.ra.public_state,
            changeDetails="s6",
        )

        # Overlaps s1 and s3
        the_future = (timezone.now() + datetime.timedelta(days=100)).date()
        s7 = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=the_future,
            state=self.ra.locked_state,
            changeDetails="s7",
        )

        d = date(1999, 1, 1)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), False)
        self.assertEqual(list(self.item.current_statuses(when=d)), [])

        d = date(2000, 1, 1)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), False)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s1])

        d = date(2005, 1, 1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s2])

        d = date(2005, 6, 29)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s2])

        d = date(2005, 6, 30)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), False)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s1])

        d = date(2005, 7, 1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s3])

        d = date(2006, 2, 1)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s4])

        d = date(2006, 3, 1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s5])

        d = date(2006, 8, 1)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s4])

        d = date(2006, 10, 31)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s4])

        d = date(2006, 11, 1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s6])

        d = date(2008, 7, 30)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s6])

        d = date(2008, 8, 1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s3])

        self.assertEqual(self.item.check_is_public(), True)
        self.assertEqual(self.item.check_is_locked(), True)
        self.assertEqual(list(self.item.current_statuses()), [s3])

        d = the_future - datetime.timedelta(days=1)
        self.assertEqual(self.item.check_is_public(when=d), True)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s3])

        d = the_future + datetime.timedelta(days=1)
        self.assertEqual(self.item.check_is_public(when=d), False)
        self.assertEqual(self.item.check_is_locked(when=d), True)
        self.assertEqual(list(self.item.current_statuses(when=d)), [s7])

    def test_object_is_public_after_ra_state_changes(self):
        self.assertEqual(self.item.is_public(), False)
        models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=models.STATES.candidate
        )
        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), False)

        self.ra.public_state = models.STATES.candidate
        self.ra.save()

        from django.core import management  # Lets recache this workgroup
        management.call_command('recache_registration_authority_item_visibility', ra=[self.ra.pk], verbosity=0)
        wait_for_signal_to_fire(seconds=10)  # Not sure if the above in async or not

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), True)

        self.ra.public_state = models.STATES.qualified
        self.ra.save()

        from django.core import management  # Lets recache this workgroup
        management.call_command('recache_registration_authority_item_visibility', ra=[self.ra.pk], verbosity=0)
        wait_for_signal_to_fire(seconds=10)  # Not sure if the above in async or not

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), False)

    def test_object_is_locked(self):
        self.assertEqual(self.item.is_locked(), False)
        s = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=models.STATES.notprogressed
        )
        self.assertEqual(self.item.is_locked(), False)

        s.state = self.ra.public_state
        s.save()

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_public(), True)

        s.state = self.ra.locked_state
        s.save()

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_locked(), True)

    def test_object_is_locked_after_ra_state_changes(self):
        self.assertEqual(self.item.is_locked(), False)
        models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=models.STATES.candidate
        )
        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_locked(), True)

        self.ra.locked_state = models.STATES.standard
        self.ra.save()

        from django.core import management  # Lets recache this RA
        management.call_command('recache_registration_authority_item_visibility', ra=[self.ra.pk], verbosity=0)
        wait_for_signal_to_fire(seconds=10)  # Not sure if the above in async or not

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_locked(), False)

        self.ra.locked_state = models.STATES.candidate
        self.ra.save()

        from django.core import management  # Lets recache this RA
        management.call_command('recache_registration_authority_item_visibility', ra=[self.ra.pk], verbosity=0)
        wait_for_signal_to_fire(seconds=10)  # Not sure if the above in async or not

        self.item = models._concept.objects.get(id=self.item.id)  # Stupid cache
        self.assertEqual(self.item.is_locked(), True)

    def test_registrar_can_view(self):
        # make editor for wg1
        r1 = get_user_model().objects.create_user('reggie@example.com', 'reg')

        self.assertEqual(perms.user_can_view(r1, self.item), False)
        models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.locked_state
        )
        self.assertEqual(perms.user_can_view(r1, self.item), False)
        # Caching issue, refresh from DB with correct permissions
        self.ra.giveRoleToUser('registrar', r1)
        r1 = get_user_model().objects.get(pk=r1.pk)

        self.assertEqual(perms.user_can_view(r1, self.item), True)

    def test_object_submitter_can_view(self):
        # make editor for wg1
        wg1 = models.Workgroup.objects.create(name="Test WG 1")
        e1 = get_user_model().objects.create_user('editor1@example.com', 'editor1')
        wg1.giveRoleToUser('submitter', e1)

        # make editor for wg2
        wg2 = models.Workgroup.objects.create(name="Test WG 2")
        e2 = get_user_model().objects.create_user('editor2@example.com', 'editor2')
        wg2.giveRoleToUser('submitter', e2)

        #RAFIX wg1.registrationAuthorities.add(self.ra)
        #RAFIX wg2.registrationAuthorities.add(self.ra)

        # ensure object is in wg1
        self.item.workgroup = wg1
        self.item.save()

        # test editor 1 can view, editor 2 cannot
        self.assertEqual(perms.user_can_view(e1, self.item), True)
        self.assertEqual(perms.user_can_view(e2, self.item), False)

        # move object to wg2
        self.item.workgroup = wg2
        self.item.save()

        # test editor 2 can view, editor 1 cannot
        self.assertEqual(perms.user_can_view(e2, self.item), True)
        self.assertEqual(perms.user_can_view(e1, self.item), False)

        s = models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.locked_state
        )
        # Editor 2 can view. Editor 1 cannot
        self.assertEqual(perms.user_can_view(e2, self.item), True)
        self.assertEqual(perms.user_can_view(e1, self.item), False)

        # Set status to a public state
        s.state = self.ra.public_state
        s.save()
        # Both can view, neither can edit.
        self.assertEqual(perms.user_can_view(e1, self.item), True)
        self.assertEqual(perms.user_can_view(e2, self.item), True)

    def test_object_submitter_can_edit(self):
        registrar = get_user_model().objects.create_user('registrar@example.com', 'registrar')
        self.ra.registrars.add(registrar)

        # make editor for wg1
        wg1 = models.Workgroup.objects.create(name="Test WG 1")
        e1 = get_user_model().objects.create_user('editor1@example.com', 'editor1')
        wg1.giveRoleToUser('submitter', e1)

        # make editor for wg2
        wg2 = models.Workgroup.objects.create(name="Test WG 2")
        e2 = get_user_model().objects.create_user('editor2@example.com', 'editor2')
        wg2.giveRoleToUser('submitter', e2)

        #RAFIX wg1.registrationAuthorities.add(self.ra)
        #RAFIX wg2.registrationAuthorities.add(self.ra)

        # ensure object is in wg1
        self.item.workgroup = wg1
        self.item.save()

        # test editor 1 can edit, editor 2 cannot
        self.assertEqual(perms.user_can_edit(e1, self.item), True)
        self.assertEqual(perms.user_can_edit(e2, self.item), False)

        # move Object Class to wg2
        self.item.workgroup = wg2
        self.item.save()

        # test editor 2 can edit, editor 1 cannot
        self.assertEqual(perms.user_can_edit(e2, self.item), True)
        self.assertEqual(perms.user_can_edit(e1, self.item), False)

        # self.ra.register(self.item,self.ra.locked_state,registrar,timezone.now(),)
        models.Status.objects.create(
            concept=self.item,
            registrationAuthority=self.ra,
            registrationDate=timezone.now(),
            state=self.ra.locked_state
        )
        # Editor 2 can no longer edit. Neither can Editor 1
        self.assertEqual(perms.user_can_edit(e2, self.item), False)
        self.assertEqual(perms.user_can_view(e1, self.item), False)


class LoggedInViewPages(object):
    """
    This helps us manage testing across different user types.
    """
    def setUp(self):
        self.wg1 = models.Workgroup.objects.create(name="Test WG 1", definition="My WG")  # Editor is member
        self.wg2 = models.Workgroup.objects.create(name="Test WG 2", definition="My WG")
        self.ra = models.RegistrationAuthority.objects.create(name="Test RA", definition="My WG")
        #RAFIX self.wg1.registrationAuthorities.add(self.ra)
        self.wg1.save()

        self.su = get_user_model().objects.create_superuser('super@example.com', 'user')
        self.manager = get_user_model().objects.create_user('mandy@example.com', 'manager')
        self.manager.is_staff=True
        self.manager.save()
        self.editor = get_user_model().objects.create_user('eddie@example.com', 'editor')
        self.editor.is_staff=True
        self.editor.save()
        self.viewer = get_user_model().objects.create_user('vicky@example.com', 'viewer')
        self.registrar = get_user_model().objects.create_user('reggie@example.com', 'registrar')
        self.ramanager = get_user_model().objects.create_user('rachael@example.com', 'ramanager')

        self.regular = get_user_model().objects.create_user('regular@example.com', 'thanks_steve')

        self.wg1.submitters.add(self.editor)
        self.wg1.managers.add(self.manager)
        self.wg1.viewers.add(self.viewer)
        self.ra.registrars.add(self.registrar)
        self.ra.managers.add(self.ramanager)

        self.editor = get_user_model().objects.get(pk=self.editor.pk)
        self.manager = get_user_model().objects.get(pk=self.manager.pk)
        self.viewer = get_user_model().objects.get(pk=self.viewer.pk)
        self.registrar = get_user_model().objects.get(pk=self.registrar.pk)
        self.ramanager = get_user_model().objects.get(pk=self.ramanager.pk)

        self.assertEqual(self.viewer.profile.editable_workgroups.count(), 0)
        self.assertEqual(self.manager.profile.editable_workgroups.count(), 0)
        self.assertEqual(self.registrar.profile.editable_workgroups.count(), 0)
        self.assertEqual(self.editor.profile.editable_workgroups.count(), 1)
        self.assertTrue(self.wg1 in self.editor.profile.editable_workgroups.all())

        self.newuser = get_user_model().objects.create_user('nathan@example.com','noobie')
        self.newuser.save()

    def get_page(self, item):
        return url_slugify_concept(item)

    def logout(self):
        self.client.post(reverse('logout'), {})

    def login_superuser(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'super@example.com', 'password': 'user'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_regular_user(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'regular@example.com', 'password': 'thanks_steve'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_viewer(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'vicky@example.com', 'password': 'viewer'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_registrar(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'reggie@example.com', 'password': 'registrar'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_ramanager(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'rachael@example.com', 'password': 'ramanager'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_editor(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'eddie@example.com', 'password': 'editor'})
        self.assertEqual(response.status_code, 302)
        return response

    def login_manager(self):
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'mandy@example.com', 'password': 'manager'})
        self.assertEqual(response.status_code, 302)
        return response

    def test_logins(self):
        # Failed logins reutrn 200, not 401
        # See http://stackoverflow.com/questions/25839434/
        response = self.client.post(reverse('friendly_login'), {'username': 'super@example.com', 'password': 'the_wrong_password'})
        self.assertEqual(response.status_code, 200)
        # Success redirects to the homepage, so its 302 not 200
        response = self.client.post(reverse('friendly_login'), {'username': 'super@example.com', 'password': 'user'})
        self.assertEqual(response.status_code, 302)
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'eddie@example.com', 'password': 'editor'})
        self.assertEqual(response.status_code, 302)
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'vicky@example.com', 'password': 'viewer'})
        self.assertEqual(response.status_code, 302)
        self.logout()
        response = self.client.post(reverse('friendly_login'), {'username': 'reggie@example.com', 'password': 'registrar'})
        self.assertEqual(response.status_code, 302)
        self.logout()

    # These are lovingly lifted from django-reversion-compare
    # https://github.com/jedie/django-reversion-compare/blob/master/tests/test_utils/test_cases.py
    def assertContainsHtml(self, response, *args):
        for html in args:
            try:
                self.assertContains(response, html, html=True)
            except AssertionError as e:  # pragma: no cover
                # Needs no coverage as the test should pass to be successful
                debug_response(response, msg="%s" % e)  # from django-tools
                raise

    def assertNotContainsHtml(self, response, *args):
        for html in args:
            try:
                self.assertNotContains(response, html, html=True)
            except AssertionError as e:  # pragma: no cover
                # Needs no coverage as the test should pass to be successful
                debug_response(response, msg="%s" % e)  # from django-tools
                raise

    def assertResponseStatusCodeEqual(self, response, code):
            try:
                self.assertEqual(response.status_code, code)
            except AssertionError as e:  # pragma: no cover
                # Needs no coverage as the test should pass to be successful
                if response.context:
                    if 'adminform' in response.context:
                        print(response.context['adminform'].form.errors.as_text())
                    elif 'form' in response.context and 'errors' in response.context['form']:
                        print(response.context['form'].form.errors.as_text())
                    elif 'errors' in response.context:
                        print(response.context['errors'])
                print(e)
                raise

    def assertDelayedEqual(self, *args):
        # This is useful when testing channels.
        # If updates aren't done in 1+2+3+4= 10seconds, then there is a problem.
        self.assertEqual(*args)
        return
        for i in range(1,5):
            try:
                self.assertEqual(*args)
                break
            except:
                print('failed, keep trying - %s',i)
                sleep(i) # sleep for progressively longer, just to give it a fighting chance to finish.
        self.assertEqual(*args)


class FormsetTestUtils:

    def get_formset_postdata(self, datalist, prefix='form', initialforms=0):

        postdata = {}
        # Add data
        index = 0
        for data in datalist:
            for key in data.keys():
                postkey = '{}-{}-{}'.format(prefix, index, key)
                postdata[postkey] = data[key]
            index += 1

        # Add management form
        postdata['{}-INITIAL_FORMS'.format(prefix)] = initialforms
        postdata['{}-TOTAL_FORMS'.format(prefix)] = index
        postdata['{}-MIN_NUM_FORMS'.format(prefix)] = 0
        postdata['{}-MAX_NUM_FORMS'.format(prefix)] = 1000

        return postdata

    def post_formset(self, url, extra_postdata={}, **kwargs):

        postdata = self.get_formset_postdata(**kwargs)
        postdata.update(extra_postdata)
        response = self.client.post(url, postdata)
        return response
