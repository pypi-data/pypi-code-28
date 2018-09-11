from unittest import TestCase
from tiipbusclient.tiipclient import TiipClient
import redis

class ClientTest(TestCase):
    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)

    def verifySubscriptions(self, app, subscriptions):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "subscribe":
                l.append(call[1][0])
        self.assertListEqual(l, subscriptions)

    def verifySubscriptionsUnordered(self, app, subscriptions):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "subscribe":
                l.append(call[1][0])
        self.assertSetEqual(set(l), set(subscriptions))

    def verifyUnsubscriptions(self, app, subscriptions):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "unsubscribe":
                l.append(call[1][0])
        self.assertListEqual(l, subscriptions)

    def verifyUnsubscriptionsUnordered(self, app, subscriptions):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "unsubscribe":
                l.append(call[1][0])
        self.assertSetEqual(set(l), set(subscriptions))

    def verifyAPI(self, app, apis):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "registerBusInterface":
                l.append(call[1][0])
        self.assertListEqual(l, apis)

    def verifyRequests(self, app, requests):
        """

        :param app:
        :param requests: [[targ, sig, arg, ]]
        :return:
        """
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "request":
                tm = call[1][0]
                l.append([tm.targ,tm.sig,tm.arg])
        self.assertListEqual(l, requests)

    def verifyReplies(self, app, replies):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "reply":
                tm = call[1][1]
                l.append([tm.ok,tm.pl])
        self.assertListEqual(l, replies)

    def verifyPublications(self, app, publications):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "publish":
                l.append(call[1][0].pl)
        self.assertListEqual(l, publications)

    def verifyPublicationsAlmostEqual(self, app, publications, places):
        l = list()
        for call in app.bc.mock_calls:
            if call[0] == "publish":
                l.append(call[1][0].pl)
        self.assertEqual(len(l),len(publications),"result size does not match: " + str(l))
        for x in range(len(publications)):
            self.assertEqual(len(l[x]), len(publications[x]), "result size does not match: " + str(l[x]))
            for y in range(len(publications[x])):
                self.assertAlmostEqual(l[x][y], publications[x][y], places, "result["+str(x)+"]["+str(y)+"] size does not match: ")

    def testInit(self):
        a = TiipClient("AUT",6379,"localhost")
        self.r = redis.StrictRedis(host=6379, port="localhost")
        self.p = self.r.pubsub()
        self.assertEqual(self.p.publish("rep/AUT", '{"pv": "tiip.2.0", "ts": "1536650962.62", "mid": "asdasdas", "type": "rep"}'))

    def testRun(self):
        a = Simulator("AUT")
        a.start()
        time.sleep(2)
        a.close()
        self.verifyPublications(a, [["Alive"]])

    def testDemo(self):
        a = Simulator("AUT")
        a.demo(TIIPMessage())
        self.verifyReplies(a, [[True,["You're Welcome"]]])