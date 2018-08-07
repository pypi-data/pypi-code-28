# This is a wrapper for PEP-0249: Python Database API Specification v2.0
import opentracing.ext.tags as ext
import wrapt

from ..tracer import internal_tracer
from ..log import logger


class CursorWrapper(wrapt.ObjectProxy):
    __slots__ = ('_module_name', '_connect_params', '_cursor_params')

    def __init__(self, cursor, module_name,
                 connect_params=None, cursor_params=None):
        super(CursorWrapper, self).__init__(wrapped=cursor)
        self._module_name = module_name
        self._connect_params = connect_params
        self._cursor_params = cursor_params

    def _collect_kvs(self, span, sql):
        try:
            span.set_tag(ext.SPAN_KIND, 'exit')
            span.set_tag(ext.DATABASE_INSTANCE, self._connect_params[1]['db'])
            span.set_tag(ext.DATABASE_STATEMENT, sql)
            span.set_tag(ext.DATABASE_TYPE, 'mysql')
            span.set_tag(ext.DATABASE_USER, self._connect_params[1]['user'])
            span.set_tag('host', "%s:%s" %
                         (self._connect_params[1]['host'],
                          self._connect_params[1]['port']))
        except Exception as e:
            logger.debug(e)
        finally:
            return span

    def execute(self, sql, params=None):
        parent_span = internal_tracer.active_span

        # If we're not tracing, just return
        if parent_span is None:
            return self.__wrapped__.execute(sql, params)

        with internal_tracer.start_active_span(self._module_name, child_of=parent_span) as scope:
            try:
                self._collect_kvs(scope.span, sql)

                result = self.__wrapped__.execute(sql, params)
            except Exception as e:
                if scope.span:
                    scope.span.log_exception(e)
                raise
            else:
                return result

    def executemany(self, sql, seq_of_parameters):
        parent_span = internal_tracer.active_span

        # If we're not tracing, just return
        if parent_span is None:
            return self.__wrapped__.executemany(sql, seq_of_parameters)

        with internal_tracer.start_active_span(self._module_name, child_of=parent_span) as scope:
            try:
                self._collect_kvs(scope.span, sql)

                result = self.__wrapped__.executemany(sql, seq_of_parameters)
            except Exception as e:
                if scope.span:
                    scope.span.log_exception(e)
                raise
            else:
                return result

    def callproc(self, proc_name, params):
        parent_span = internal_tracer.active_span

        # If we're not tracing, just return
        if parent_span is None:
            return self.__wrapped__.execute(proc_name, params)

        with internal_tracer.start_active_span(self._module_name, child_of=parent_span) as scope:
            try:
                self._collect_kvs(scope.span, proc_name)

                result = self.__wrapped__.callproc(proc_name, params)
            except Exception as e:
                if scope.span:
                    scope.span.log_exception(e)
                raise
            else:
                return result


class ConnectionWrapper(wrapt.ObjectProxy):
    __slots__ = ('_module_name', '_connect_params')

    def __init__(self, connection, module_name, connect_params):
        super(ConnectionWrapper, self).__init__(wrapped=connection)
        self._module_name = module_name
        self._connect_params = connect_params

    def cursor(self, *args, **kwargs):
        return CursorWrapper(
            cursor=self.__wrapped__.cursor(*args, **kwargs),
            module_name=self._module_name,
            connect_params=self._connect_params,
            cursor_params=(args, kwargs) if args or kwargs else None)

    def begin(self):
        return self.__wrapped__.begin()

    def commit(self):
        return self.__wrapped__.commit()

    def rollback(self):
        return self.__wrapped__.rollback()


class ConnectionFactory(object):
    def __init__(self, connect_func, module_name):
        self._connect_func = connect_func
        self._module_name = module_name
        self._wrapper_ctor = ConnectionWrapper

    def __call__(self, *args, **kwargs):
        connect_params = (args, kwargs) if args or kwargs else None

        return self._wrapper_ctor(
            connection=self._connect_func(*args, **kwargs),
            module_name=self._module_name,
            connect_params=connect_params)
