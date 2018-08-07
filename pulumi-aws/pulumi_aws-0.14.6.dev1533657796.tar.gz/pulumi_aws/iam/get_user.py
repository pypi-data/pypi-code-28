# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class GetUserResult(object):
    """
    A collection of values returned by getUser.
    """
    def __init__(__self__, arn=None, path=None, user_id=None, id=None):
        if arn and not isinstance(arn, basestring):
            raise TypeError('Expected argument arn to be a basestring')
        __self__.arn = arn
        """
        The Amazon Resource Name (ARN) assigned by AWS for this user.
        """
        if path and not isinstance(path, basestring):
            raise TypeError('Expected argument path to be a basestring')
        __self__.path = path
        """
        Path in which this user was created.
        """
        if user_id and not isinstance(user_id, basestring):
            raise TypeError('Expected argument user_id to be a basestring')
        __self__.user_id = user_id
        """
        The unique ID assigned by AWS for this user.
        """
        if id and not isinstance(id, basestring):
            raise TypeError('Expected argument id to be a basestring')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

def get_user(user_name=None):
    """
    This data source can be used to fetch information about a specific
    IAM user. By using this data source, you can reference IAM user
    properties without having to hard code ARNs or unique IDs as input.
    """
    __args__ = dict()

    __args__['userName'] = user_name
    __ret__ = pulumi.runtime.invoke('aws:iam/getUser:getUser', __args__)

    return GetUserResult(
        arn=__ret__.get('arn'),
        path=__ret__.get('path'),
        user_id=__ret__.get('userId'),
        id=__ret__.get('id'))
