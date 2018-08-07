# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class GetRoleResult(object):
    """
    A collection of values returned by getRole.
    """
    def __init__(__self__, arn=None, assume_role_policy=None, assume_role_policy_document=None, create_date=None, description=None, max_session_duration=None, path=None, role_id=None, unique_id=None, id=None):
        if arn and not isinstance(arn, basestring):
            raise TypeError('Expected argument arn to be a basestring')
        __self__.arn = arn
        """
        The Amazon Resource Name (ARN) specifying the role.
        """
        if assume_role_policy and not isinstance(assume_role_policy, basestring):
            raise TypeError('Expected argument assume_role_policy to be a basestring')
        __self__.assume_role_policy = assume_role_policy
        """
        The policy document associated with the role.
        """
        if assume_role_policy_document and not isinstance(assume_role_policy_document, basestring):
            raise TypeError('Expected argument assume_role_policy_document to be a basestring')
        __self__.assume_role_policy_document = assume_role_policy_document
        if create_date and not isinstance(create_date, basestring):
            raise TypeError('Expected argument create_date to be a basestring')
        __self__.create_date = create_date
        if description and not isinstance(description, basestring):
            raise TypeError('Expected argument description to be a basestring')
        __self__.description = description
        if max_session_duration and not isinstance(max_session_duration, int):
            raise TypeError('Expected argument max_session_duration to be a int')
        __self__.max_session_duration = max_session_duration
        if path and not isinstance(path, basestring):
            raise TypeError('Expected argument path to be a basestring')
        __self__.path = path
        """
        The path to the role.
        """
        if role_id and not isinstance(role_id, basestring):
            raise TypeError('Expected argument role_id to be a basestring')
        __self__.role_id = role_id
        if unique_id and not isinstance(unique_id, basestring):
            raise TypeError('Expected argument unique_id to be a basestring')
        __self__.unique_id = unique_id
        """
        The stable and unique string identifying the role.
        """
        if id and not isinstance(id, basestring):
            raise TypeError('Expected argument id to be a basestring')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

def get_role(name=None, role_name=None):
    """
    This data source can be used to fetch information about a specific
    IAM role. By using this data source, you can reference IAM role
    properties without having to hard code ARNs as input.
    """
    __args__ = dict()

    __args__['name'] = name
    __args__['roleName'] = role_name
    __ret__ = pulumi.runtime.invoke('aws:iam/getRole:getRole', __args__)

    return GetRoleResult(
        arn=__ret__.get('arn'),
        assume_role_policy=__ret__.get('assumeRolePolicy'),
        assume_role_policy_document=__ret__.get('assumeRolePolicyDocument'),
        create_date=__ret__.get('createDate'),
        description=__ret__.get('description'),
        max_session_duration=__ret__.get('maxSessionDuration'),
        path=__ret__.get('path'),
        role_id=__ret__.get('roleId'),
        unique_id=__ret__.get('uniqueId'),
        id=__ret__.get('id'))
