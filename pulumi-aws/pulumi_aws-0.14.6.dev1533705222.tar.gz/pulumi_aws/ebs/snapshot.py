# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class Snapshot(pulumi.CustomResource):
    """
    Creates a Snapshot of an EBS Volume.
    """
    def __init__(__self__, __name__, __opts__=None, description=None, tags=None, volume_id=None):
        """Create a Snapshot resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        A description of what the snapshot is.
        """
        __props__['description'] = description

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the snapshot
        """
        __props__['tags'] = tags

        if not volume_id:
            raise TypeError('Missing required property volume_id')
        elif not isinstance(volume_id, basestring):
            raise TypeError('Expected property volume_id to be a basestring')
        __self__.volume_id = volume_id
        """
        The Volume ID of which to make a snapshot.
        """
        __props__['volumeId'] = volume_id

        __self__.data_encryption_key_id = pulumi.runtime.UNKNOWN
        """
        The data encryption key identifier for the snapshot.
        """
        __self__.encrypted = pulumi.runtime.UNKNOWN
        """
        Whether the snapshot is encrypted.
        """
        __self__.kms_key_id = pulumi.runtime.UNKNOWN
        """
        The ARN for the KMS encryption key.
        """
        __self__.owner_alias = pulumi.runtime.UNKNOWN
        """
        Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        """
        __self__.owner_id = pulumi.runtime.UNKNOWN
        """
        The AWS account ID of the EBS snapshot owner.
        """
        __self__.volume_size = pulumi.runtime.UNKNOWN
        """
        The size of the drive in GiBs.
        """

        super(Snapshot, __self__).__init__(
            'aws:ebs/snapshot:Snapshot',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'dataEncryptionKeyId' in outs:
            self.data_encryption_key_id = outs['dataEncryptionKeyId']
        if 'description' in outs:
            self.description = outs['description']
        if 'encrypted' in outs:
            self.encrypted = outs['encrypted']
        if 'kmsKeyId' in outs:
            self.kms_key_id = outs['kmsKeyId']
        if 'ownerAlias' in outs:
            self.owner_alias = outs['ownerAlias']
        if 'ownerId' in outs:
            self.owner_id = outs['ownerId']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'volumeId' in outs:
            self.volume_id = outs['volumeId']
        if 'volumeSize' in outs:
            self.volume_size = outs['volumeSize']
