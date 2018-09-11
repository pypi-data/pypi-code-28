#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from __future__ import absolute_import
from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from mastercarddisbursements import ResourceConfig

class ConsumerAccount(BaseObject):
    """
    
    """

    __config = {
        
        "957f1e35-4427-4a90-87f8-a8e0c77dce75" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts", "create", [], []),
        
        "70a5b6a1-17e4-45da-9993-30f679c847e6" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "delete", [], []),
        
        "480b6e59-6fc2-462f-bcdf-5cc9aefe751a" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "read", [], []),
        
        "84e2126b-7a4d-40e5-a73b-27612cd975a5" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts", "query", [], ["ref"]),
        
        "7e20a8ee-73d5-41c8-aced-f1faf97c716d" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUID)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative(), ResourceConfig.getInstance().getContentTypeOverride())


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerAccount

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerAccount of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("957f1e35-4427-4a90-87f8-a8e0c77dce75", ConsumerAccount(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerAccount by id

        @param str id
        @return ConsumerAccount of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("70a5b6a1-17e4-45da-9993-30f679c847e6", ConsumerAccount(mapObj))

    def delete(self):
        """
        Delete object of type ConsumerAccount

        @return ConsumerAccount of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("70a5b6a1-17e4-45da-9993-30f679c847e6", self)







    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type ConsumerAccount by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerAccount
        @raise ApiException: raised an exception from the response status
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("480b6e59-6fc2-462f-bcdf-5cc9aefe751a", ConsumerAccount(mapObj))







    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerAccount by id and optional criteria
        @param type criteria
        @return ConsumerAccount object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("84e2126b-7a4d-40e5-a73b-27612cd975a5", ConsumerAccount(criteria))


    def update(self):
        """
        Updates an object of type ConsumerAccount

        @return ConsumerAccount object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("7e20a8ee-73d5-41c8-aced-f1faf97c716d", self)






