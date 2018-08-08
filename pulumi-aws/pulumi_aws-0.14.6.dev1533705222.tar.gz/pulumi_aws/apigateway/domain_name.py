# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class DomainName(pulumi.CustomResource):
    """
    Registers a custom domain name for use with AWS API Gateway.
    
    This resource just establishes ownership of and the TLS settings for
    a particular domain name. An API can be attached to a particular path
    under the registered domain name using
    [the `aws_api_gateway_base_path_mapping` resource](api_gateway_base_path_mapping.html).
    
    API Gateway domains can be defined as either 'edge-optimized' or 'regional'.  In an edge-optimized configuration,
    API Gateway internally creates and manages a CloudFront distribution to route requests on the given hostname. In
    addition to this resource it's necessary to create a DNS record corresponding to the given domain name which is an alias
    (either Route53 alias or traditional CNAME) to the Cloudfront domain name exported in the `cloudfront_domain_name`
    attribute.
    
    In a regional configuration, API Gateway does not create a CloudFront distribution to route requests to the API, though
    a distribution can be created if needed. In either case, it is necessary to create a DNS record corresponding to the
    given domain name which is an alias (either Route53 alias or traditional CNAME) to the regional domain name exported in
    the `regional_domain_name` attribute.
    
    ~> **Note:** All arguments including the private key will be stored in the raw state as plain-text.
    [Read more about sensitive data in state](/docs/state/sensitive-data.html).
    """
    def __init__(__self__, __name__, __opts__=None, certificate_arn=None, certificate_body=None, certificate_chain=None, certificate_name=None, certificate_private_key=None, domain_name=None, endpoint_configuration=None, regional_certificate_arn=None, regional_certificate_name=None):
        """Create a DomainName resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if certificate_arn and not isinstance(certificate_arn, basestring):
            raise TypeError('Expected property certificate_arn to be a basestring')
        __self__.certificate_arn = certificate_arn
        """
        The ARN for an AWS-managed certificate. Used when an edge-optimized domain name is
        desired. Conflicts with `certificate_name`, `certificate_body`, `certificate_chain`, `certificate_private_key`,
        `regional_certificate_arn`, and `regional_certificate_name`.
        """
        __props__['certificateArn'] = certificate_arn

        if certificate_body and not isinstance(certificate_body, basestring):
            raise TypeError('Expected property certificate_body to be a basestring')
        __self__.certificate_body = certificate_body
        """
        The certificate issued for the domain name
        being registered, in PEM format. Only valid for `EDGE` endpoint configuration type. Conflicts with `certificate_arn`, `regional_certificate_arn`, and
        `regional_certificate_name`.
        """
        __props__['certificateBody'] = certificate_body

        if certificate_chain and not isinstance(certificate_chain, basestring):
            raise TypeError('Expected property certificate_chain to be a basestring')
        __self__.certificate_chain = certificate_chain
        """
        The certificate for the CA that issued the
        certificate, along with any intermediate CA certificates required to
        create an unbroken chain to a certificate trusted by the intended API clients. Only valid for `EDGE` endpoint configuration type. Conflicts with `certificate_arn`,
        `regional_certificate_arn`, and `regional_certificate_name`.
        """
        __props__['certificateChain'] = certificate_chain

        if certificate_name and not isinstance(certificate_name, basestring):
            raise TypeError('Expected property certificate_name to be a basestring')
        __self__.certificate_name = certificate_name
        """
        The unique name to use when registering this
        certificate as an IAM server certificate. Conflicts with `certificate_arn`, `regional_certificate_arn`, and
        `regional_certificate_name`. Required if `certificate_arn` is not set.
        """
        __props__['certificateName'] = certificate_name

        if certificate_private_key and not isinstance(certificate_private_key, basestring):
            raise TypeError('Expected property certificate_private_key to be a basestring')
        __self__.certificate_private_key = certificate_private_key
        """
        The private key associated with the
        domain certificate given in `certificate_body`. Only valid for `EDGE` endpoint configuration type. Conflicts with `certificate_arn`, `regional_certificate_arn`, and `regional_certificate_name`.
        """
        __props__['certificatePrivateKey'] = certificate_private_key

        if not domain_name:
            raise TypeError('Missing required property domain_name')
        elif not isinstance(domain_name, basestring):
            raise TypeError('Expected property domain_name to be a basestring')
        __self__.domain_name = domain_name
        """
        The fully-qualified domain name to register
        """
        __props__['domainName'] = domain_name

        if endpoint_configuration and not isinstance(endpoint_configuration, dict):
            raise TypeError('Expected property endpoint_configuration to be a dict')
        __self__.endpoint_configuration = endpoint_configuration
        """
        Nested argument defining API endpoint configuration including endpoint type. Defined below.
        """
        __props__['endpointConfiguration'] = endpoint_configuration

        if regional_certificate_arn and not isinstance(regional_certificate_arn, basestring):
            raise TypeError('Expected property regional_certificate_arn to be a basestring')
        __self__.regional_certificate_arn = regional_certificate_arn
        """
        The ARN for an AWS-managed certificate. Used when a regional domain name is
        desired. Conflicts with `certificate_arn`, `certificate_name`, `certificate_body`, `certificate_chain`, and
        `certificate_private_key`.
        """
        __props__['regionalCertificateArn'] = regional_certificate_arn

        if regional_certificate_name and not isinstance(regional_certificate_name, basestring):
            raise TypeError('Expected property regional_certificate_name to be a basestring')
        __self__.regional_certificate_name = regional_certificate_name
        """
        The user-friendly name of the certificate that will be used by regional endpoint for this domain name. Conflicts with `certificate_arn`, `certificate_name`, `certificate_body`, `certificate_chain`, and
        `certificate_private_key`.
        """
        __props__['regionalCertificateName'] = regional_certificate_name

        __self__.certificate_upload_date = pulumi.runtime.UNKNOWN
        """
        The upload date associated with the domain certificate.
        """
        __self__.cloudfront_domain_name = pulumi.runtime.UNKNOWN
        """
        The hostname created by Cloudfront to represent
        the distribution that implements this domain name mapping.
        """
        __self__.cloudfront_zone_id = pulumi.runtime.UNKNOWN
        """
        For convenience, the hosted zone ID (`Z2FDTNDATAQYW2`)
        that can be used to create a Route53 alias record for the distribution.
        """
        __self__.regional_domain_name = pulumi.runtime.UNKNOWN
        """
        The hostname for the custom domain's regional endpoint.
        """
        __self__.regional_zone_id = pulumi.runtime.UNKNOWN
        """
        The hosted zone ID that can be used to create a Route53 alias record for the regional endpoint.
        """

        super(DomainName, __self__).__init__(
            'aws:apigateway/domainName:DomainName',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'certificateArn' in outs:
            self.certificate_arn = outs['certificateArn']
        if 'certificateBody' in outs:
            self.certificate_body = outs['certificateBody']
        if 'certificateChain' in outs:
            self.certificate_chain = outs['certificateChain']
        if 'certificateName' in outs:
            self.certificate_name = outs['certificateName']
        if 'certificatePrivateKey' in outs:
            self.certificate_private_key = outs['certificatePrivateKey']
        if 'certificateUploadDate' in outs:
            self.certificate_upload_date = outs['certificateUploadDate']
        if 'cloudfrontDomainName' in outs:
            self.cloudfront_domain_name = outs['cloudfrontDomainName']
        if 'cloudfrontZoneId' in outs:
            self.cloudfront_zone_id = outs['cloudfrontZoneId']
        if 'domainName' in outs:
            self.domain_name = outs['domainName']
        if 'endpointConfiguration' in outs:
            self.endpoint_configuration = outs['endpointConfiguration']
        if 'regionalCertificateArn' in outs:
            self.regional_certificate_arn = outs['regionalCertificateArn']
        if 'regionalCertificateName' in outs:
            self.regional_certificate_name = outs['regionalCertificateName']
        if 'regionalDomainName' in outs:
            self.regional_domain_name = outs['regionalDomainName']
        if 'regionalZoneId' in outs:
            self.regional_zone_id = outs['regionalZoneId']
