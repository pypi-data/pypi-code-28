# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime

class DeploymentGroup(pulumi.CustomResource):
    """
    Provides a CodeDeploy Deployment Group for a CodeDeploy Application
    """
    def __init__(__self__, __name__, __opts__=None, alarm_configuration=None, app_name=None, auto_rollback_configuration=None, autoscaling_groups=None, blue_green_deployment_config=None, deployment_config_name=None, deployment_group_name=None, deployment_style=None, ec2_tag_filters=None, ec2_tag_sets=None, load_balancer_info=None, on_premises_instance_tag_filters=None, service_role_arn=None, trigger_configurations=None):
        """Create a DeploymentGroup resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if alarm_configuration and not isinstance(alarm_configuration, dict):
            raise TypeError('Expected property alarm_configuration to be a dict')
        __self__.alarm_configuration = alarm_configuration
        """
        Information about alarms associated with the deployment group (documented below).
        """
        __props__['alarmConfiguration'] = alarm_configuration

        if not app_name:
            raise TypeError('Missing required property app_name')
        elif not isinstance(app_name, basestring):
            raise TypeError('Expected property app_name to be a basestring')
        __self__.app_name = app_name
        """
        The name of the application.
        """
        __props__['appName'] = app_name

        if auto_rollback_configuration and not isinstance(auto_rollback_configuration, dict):
            raise TypeError('Expected property auto_rollback_configuration to be a dict')
        __self__.auto_rollback_configuration = auto_rollback_configuration
        """
        The automatic rollback configuration associated with the deployment group (documented below).
        """
        __props__['autoRollbackConfiguration'] = auto_rollback_configuration

        if autoscaling_groups and not isinstance(autoscaling_groups, list):
            raise TypeError('Expected property autoscaling_groups to be a list')
        __self__.autoscaling_groups = autoscaling_groups
        """
        Autoscaling groups associated with the deployment group.
        """
        __props__['autoscalingGroups'] = autoscaling_groups

        if blue_green_deployment_config and not isinstance(blue_green_deployment_config, dict):
            raise TypeError('Expected property blue_green_deployment_config to be a dict')
        __self__.blue_green_deployment_config = blue_green_deployment_config
        """
        Information about blue/green deployment options for a deployment group (documented below).
        """
        __props__['blueGreenDeploymentConfig'] = blue_green_deployment_config

        if deployment_config_name and not isinstance(deployment_config_name, basestring):
            raise TypeError('Expected property deployment_config_name to be a basestring')
        __self__.deployment_config_name = deployment_config_name
        """
        The name of the group's deployment config. The default is "CodeDeployDefault.OneAtATime".
        """
        __props__['deploymentConfigName'] = deployment_config_name

        if not deployment_group_name:
            raise TypeError('Missing required property deployment_group_name')
        elif not isinstance(deployment_group_name, basestring):
            raise TypeError('Expected property deployment_group_name to be a basestring')
        __self__.deployment_group_name = deployment_group_name
        """
        The name of the deployment group.
        """
        __props__['deploymentGroupName'] = deployment_group_name

        if deployment_style and not isinstance(deployment_style, dict):
            raise TypeError('Expected property deployment_style to be a dict')
        __self__.deployment_style = deployment_style
        """
        Information about the type of deployment, either in-place or blue/green, you want to run and whether to route deployment traffic behind a load balancer (documented below).
        """
        __props__['deploymentStyle'] = deployment_style

        if ec2_tag_filters and not isinstance(ec2_tag_filters, list):
            raise TypeError('Expected property ec2_tag_filters to be a list')
        __self__.ec2_tag_filters = ec2_tag_filters
        """
        Tag filters associated with the deployment group. See the AWS docs for details.
        """
        __props__['ec2TagFilters'] = ec2_tag_filters

        if ec2_tag_sets and not isinstance(ec2_tag_sets, list):
            raise TypeError('Expected property ec2_tag_sets to be a list')
        __self__.ec2_tag_sets = ec2_tag_sets
        """
        Sets of Tag filters associated with the deployment group, which are referred to as *tag groups* in the document.  See the AWS docs for details.
        """
        __props__['ec2TagSets'] = ec2_tag_sets

        if load_balancer_info and not isinstance(load_balancer_info, dict):
            raise TypeError('Expected property load_balancer_info to be a dict')
        __self__.load_balancer_info = load_balancer_info
        """
        Information about the load balancer to use in a blue/green deployment (documented below).
        """
        __props__['loadBalancerInfo'] = load_balancer_info

        if on_premises_instance_tag_filters and not isinstance(on_premises_instance_tag_filters, list):
            raise TypeError('Expected property on_premises_instance_tag_filters to be a list')
        __self__.on_premises_instance_tag_filters = on_premises_instance_tag_filters
        """
        On premise tag filters associated with the group. See the AWS docs for details.
        """
        __props__['onPremisesInstanceTagFilters'] = on_premises_instance_tag_filters

        if not service_role_arn:
            raise TypeError('Missing required property service_role_arn')
        elif not isinstance(service_role_arn, basestring):
            raise TypeError('Expected property service_role_arn to be a basestring')
        __self__.service_role_arn = service_role_arn
        """
        The service role ARN that allows deployments.
        """
        __props__['serviceRoleArn'] = service_role_arn

        if trigger_configurations and not isinstance(trigger_configurations, list):
            raise TypeError('Expected property trigger_configurations to be a list')
        __self__.trigger_configurations = trigger_configurations
        """
        Trigger Configurations for the deployment group (documented below).
        """
        __props__['triggerConfigurations'] = trigger_configurations

        super(DeploymentGroup, __self__).__init__(
            'aws:codedeploy/deploymentGroup:DeploymentGroup',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'alarmConfiguration' in outs:
            self.alarm_configuration = outs['alarmConfiguration']
        if 'appName' in outs:
            self.app_name = outs['appName']
        if 'autoRollbackConfiguration' in outs:
            self.auto_rollback_configuration = outs['autoRollbackConfiguration']
        if 'autoscalingGroups' in outs:
            self.autoscaling_groups = outs['autoscalingGroups']
        if 'blueGreenDeploymentConfig' in outs:
            self.blue_green_deployment_config = outs['blueGreenDeploymentConfig']
        if 'deploymentConfigName' in outs:
            self.deployment_config_name = outs['deploymentConfigName']
        if 'deploymentGroupName' in outs:
            self.deployment_group_name = outs['deploymentGroupName']
        if 'deploymentStyle' in outs:
            self.deployment_style = outs['deploymentStyle']
        if 'ec2TagFilters' in outs:
            self.ec2_tag_filters = outs['ec2TagFilters']
        if 'ec2TagSets' in outs:
            self.ec2_tag_sets = outs['ec2TagSets']
        if 'loadBalancerInfo' in outs:
            self.load_balancer_info = outs['loadBalancerInfo']
        if 'onPremisesInstanceTagFilters' in outs:
            self.on_premises_instance_tag_filters = outs['onPremisesInstanceTagFilters']
        if 'serviceRoleArn' in outs:
            self.service_role_arn = outs['serviceRoleArn']
        if 'triggerConfigurations' in outs:
            self.trigger_configurations = outs['triggerConfigurations']
