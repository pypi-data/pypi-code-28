import asyncio
from asyncio import FIRST_COMPLETED
import os
import uuid

import aiodns

from .util import ClosableQueue, QueueClosed, read_nameservers_from_file


Token = 1


class ResolverWorker:
    """Connects to a single nameserver with multiple workers.

    Rate-limited with a simplified version of the token bucket algorithm.
    """

    def __init__(self, loop, nameserver, wildcard_responses=None):
        self._wildcard_responses = wildcard_responses

        self._resolver = aiodns.DNSResolver(loop=loop, nameservers=[nameserver])
        self._token_queue = asyncio.Queue()

        rate = 100  # per second
        self._interval = 1/rate
        self._coroutines = 10

    async def _matches_wildcard(self, name, resp):
        if self._wildcard_responses is None:
            return False

        parent_domain = name.split(".", 1)[1]
        if parent_domain not in self._wildcard_responses:
            wildcard = str(uuid.uuid4()) + "." + parent_domain
            try:
                r = await self._resolver.query(wildcard, "A")
                wildcard_resp = set(h.host for h in r)
            except (aiodns.error.DNSError, UnicodeError, IndexError):
                wildcard_resp = None

            self._wildcard_responses[parent_domain] = wildcard_resp
        else:
            wildcard_resp = self._wildcard_responses[parent_domain]

        return wildcard_resp == set(h.host for h in resp)

    async def _query(self, name):
        for query_type in ["A", "AAAA"]:
            await self._token_queue.get()
            try:
                resp = await self._resolver.query(name, query_type)
                if await self._matches_wildcard(name, resp):
                    return None
                return resp[0].host
            except (aiodns.error.DNSError, UnicodeError, IndexError):
                continue
        return None

    async def _worker(self, host_queue, resolved_queue):
        while True:
            try:
                host = await host_queue.get()
            except QueueClosed:
                break
            resolved = await self._query(host)
            if resolved:
                await resolved_queue.put((host, resolved))

    async def _feed_tokens(self):
        while True:
            await self._token_queue.put(Token)
            await asyncio.sleep(self._interval)

    async def resolve_from_queue(self, host_queue, resolved_queue):
        token_feeder = asyncio.ensure_future(self._feed_tokens())
        workers = [self._worker(host_queue, resolved_queue) for _ in range(self._coroutines)]

        await asyncio.wait([token_feeder, asyncio.gather(*workers)], return_when=FIRST_COMPLETED)
        token_feeder.cancel()


class Resolver:
    """A resolver that spawns a ResolverWorker for each nameserver provided.
    """

    def __init__(self, nameservers=None, detect_wildcard_dns=True):
        if not nameservers:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            nameservers = read_nameservers_from_file(current_dir + "/data/nameservers.txt")

        if detect_wildcard_dns:
            wildcard_responses = {}
        else:
            wildcard_responses = None

        self.loop = asyncio.get_event_loop()
        self._resolvers = []
        for ns in nameservers:
            self._resolvers.append(ResolverWorker(self.loop, ns, wildcard_responses))

    async def _feed_hosts(self, hosts, outqueue):
        for host in hosts:
            await outqueue.put(host)

        outqueue.close()

    async def _resolve_hosts(self, hosts):
        host_queue = ClosableQueue()
        resolved_queue = asyncio.Queue()
        resolver_futures = []
        for resolver in self._resolvers:
            resolver_futures.append(resolver.resolve_from_queue(host_queue, resolved_queue))

        await asyncio.gather(self._feed_hosts(hosts, host_queue), *resolver_futures)

        return list(resolved_queue._queue)  # pylint: disable=protected-access

    def resolve_hosts(self, hosts):
        return self.loop.run_until_complete(self._resolve_hosts(hosts))
