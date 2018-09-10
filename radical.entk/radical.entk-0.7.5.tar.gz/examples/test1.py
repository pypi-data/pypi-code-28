import radical.pilot as rp
from multiprocessing import Process
import traceback

def func(umgr):

    try:
        cud = rp.ComputeUnitDescription()
        cud.executable = '/bin/date'
        print umgr.uid
        umgr.submit_units(cud)
    except Exception as ex:
        print ex
        print traceback.format_exc()

if __name__ == '__main__':

    session = rp.Session()
    umgr = rp.UnitManager(session=session)
    pmgr = rp.PilotManager(session=session)

    pd_init = {'resource': 'local.localhost',
                'runtime': 15,  # pilot runtime (min)
                'cores': 1
                }
    pdesc = rp.ComputePilotDescription(pd_init)
    pilot = pmgr.submit_pilots(pdesc)
    umgr.add_pilots(pilot)

    p = Process(target=func, args=(umgr,))
    p.start()
    p.join()
    p = Process(target=func, args=(umgr,))
    p.start()
    p.join()
