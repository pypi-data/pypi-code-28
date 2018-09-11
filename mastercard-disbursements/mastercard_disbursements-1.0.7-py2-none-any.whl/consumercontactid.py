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

class ConsumerContactID(BaseObject):
    """
    
    """

    __config = {
        
        "e6bfb26f-61b2-40bc-aab2-fc5f4271c4ba" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "create", [], []),
        
        "11985127-6441-43fc-a056-1e98854d755d" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "delete", [], []),
        
        "58cb490d-f8c4-43e7-9f8d-1ea64353fa92" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "read", [], []),
        
        "fa073b38-1966-4e5d-bbd6-5be0c5502860" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "query", [], []),
        
        "cf6c7192-4034-41af-979d-63bee9fda9ea" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "update", [], []),
        
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
        Creates object of type ConsumerContactID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerContactID of the response of created instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("e6bfb26f-61b2-40bc-aab2-fc5f4271c4ba", ConsumerContactID(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerContactID by id

        @param str id
        @return ConsumerContactID of the response of the deleted instance.
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

        return BaseObject.execute("11985127-6441-43fc-a056-1e98854d755d", ConsumerContactID(mapObj))

    def delete(self):
        """
        Delete object of type ConsumerContactID

        @return ConsumerContactID of the response of the deleted instance.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("11985127-6441-43fc-a056-1e98854d755d", self)







    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerContactID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerContactID
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

        return BaseObject.execute("58cb490d-f8c4-43e7-9f8d-1ea64353fa92", ConsumerContactID(mapObj))







    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerContactID by id and optional criteria
        @param type criteria
        @return ConsumerContactID object representing the response.
        @raise ApiException: raised an exception from the response status
        """

        return BaseObject.execute("fa073b38-1966-4e5d-bbd6-5be0c5502860", ConsumerContactID(criteria))


    def update(self):
        """
        Updates an object of type ConsumerContactID

        @return ConsumerContactID object representing the response.
        @raise ApiException: raised an exception from the response status
        """
        return BaseObject.execute("cf6c7192-4034-41af-979d-63bee9fda9ea", self)






