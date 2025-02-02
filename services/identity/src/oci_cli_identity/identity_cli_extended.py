# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function
import click
import six
import sys
from oci_cli_identity.generated import identity_cli
from oci_cli import cli_util
from oci_cli import cli_exceptions
from oci_cli import custom_types
from oci_cli import json_skeleton_utils


identity_cli.iam_root_group.commands.pop(identity_cli.idp_group_mapping_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.tenancy_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.user_group_membership_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.identity_provider_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.api_key_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.swift_password_group.name)
identity_cli.iam_root_group.commands.pop(identity_cli.ui_password_group.name)

identity_cli.user_group.add_command(identity_cli.api_key_group)
identity_cli.user_group.add_command(identity_cli.swift_password_group)
identity_cli.user_group.add_command(identity_cli.ui_password_group)

identity_cli.tag_group.commands.pop(identity_cli.update_tag.name)

identity_cli.tag_namespace_group.commands.pop(identity_cli.update_tag_namespace.name)

identity_cli.api_key_group.commands.pop(identity_cli.upload_api_key.name)

cli_util.get_param(identity_cli.create_policy, 'version_date').type = click.STRING

# help for oci iam policy create --statements
identity_policy_create_statements_example = """'["statement 1","statement 2"]'"""
identity_policy_create_statements_help = cli_util.GENERIC_JSON_FORMAT_HELP
cli_util.update_param_help(identity_cli.create_policy, 'statements', identity_policy_create_statements_help, append=True, example=identity_policy_create_statements_example)

# revised short help for tagging operations
identity_cli.create_tag.short_help = 'Create new tag in a given tagNamespace'
identity_cli.get_tag.short_help = 'Gets the specified tag''s information'
identity_cli.list_tags.short_help = 'List tags in a given tagNamespace'
identity_cli.create_tag_namespace.short_help = 'Create new tagNamespace in a compartment'
identity_cli.get_tag_namespace.short_help = 'Get a tagNamespace''s information'
identity_cli.list_tag_namespaces.short_help = 'List the tagNamespaces in a compartment'


@identity_cli.user_group.command(name='list-groups', help="""Lists the groups for which the specified user is a member. You must specify your tenancy's OCID as the value for the compartment ID (remember that the tenancy is simply the root compartment). See [Where to Get the Tenancy's OCID and User's OCID].""")
@cli_util.option('--compartment-id', required=True, help="""The OCID of the compartment (remember that the tenancy is simply the root compartment).""")
@cli_util.option('--user-id', required=True, help="""The OCID of the user.""")
@cli_util.option('--page', help="""The value of the `opc-next-page` response header from the previous \"List\" call.""")
@cli_util.option('--limit', type=click.INT, help="""The maximum number of items to return in a paginated \"List\" call.""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'list[Group]'})
@cli_util.wrap_exceptions
def list_groups_for_user(ctx, from_json, compartment_id, user_id, page, limit, all_pages, page_size):
    cli_util.load_context_obj_values_from_defaults(ctx)
    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    client = cli_util.build_client('identity', ctx)
    args = {}

    args['user_id'] = user_id

    if page is not None:
        args['page'] = page

    if limit is not None:
        args['limit'] = limit

    if all_pages:
        if page_size:
            args['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_user_group_memberships,
            compartment_id=compartment_id,
            **args
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_user_group_memberships,
            limit,
            page_size,
            compartment_id=compartment_id,
            **args
        )
    else:
        result = client.list_user_group_memberships(compartment_id=compartment_id, ** args)

    groups = []

    for membership in result.data:
        groups.append(client.get_group(membership.group_id).data)

    cli_util.render(groups, result.headers, ctx)


@identity_cli.group_group.command(name='list-users', help="""Lists the users in the specified group. You must specify your tenancy's OCID as the value for the compartment ID (remember that the tenancy is simply the root compartment). See [Where to Get the Tenancy's OCID and User's OCID].""")
@cli_util.option('--compartment-id', required=True,
                 help="""The OCID of the compartment (remember that the tenancy is simply the root compartment).""")
@cli_util.option('--group-id', required=True, help="""The OCID of the user.""")
@cli_util.option('--page',
                 help="""The value of the `opc-next-page` response header from the previous \"List\" call.""")
@cli_util.option('--limit', type=click.INT, help="""The maximum number of items to return in a paginated \"List\" call.""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'list[User]'})
@cli_util.wrap_exceptions
def list_users_for_group(ctx, from_json, compartment_id, group_id, page, limit, all_pages, page_size):
    cli_util.load_context_obj_values_from_defaults(ctx)
    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    client = cli_util.build_client('identity', ctx)
    args = {}

    args['group_id'] = group_id

    if page is not None:
        args['page'] = page

    if limit is not None:
        args['limit'] = limit

    if all_pages:
        if page_size:
            args['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_user_group_memberships,
            compartment_id=compartment_id,
            **args
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_user_group_memberships,
            limit,
            page_size,
            compartment_id=compartment_id,
            **args
        )
    else:
        result = client.list_user_group_memberships(compartment_id=compartment_id, **args)

    users = []

    for membership in result.data:
        users.append(client.get_user(membership.user_id).data)

    cli_util.render(users, result.headers, ctx)


@identity_cli.group_group.command(name='add-user', help="""Adds the specified user to the specified group.""")
@cli_util.option('--user-id', required=True, help="""The OCID of the user.""")
@cli_util.option('--group-id', required=True, help="""The OCID of the group.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'UserGroupMembership'})
@cli_util.wrap_exceptions
def add_user_to_group(ctx, from_json, user_id, group_id):
    cli_util.load_context_obj_values_from_defaults(ctx)
    client = cli_util.build_client('identity', ctx)
    result = client.add_user_to_group(add_user_to_group_details={"userId": user_id, "groupId": group_id})
    cli_util.render_response(result, ctx)


@identity_cli.group_group.command(name='remove-user', help="""Removes a user from a group.""")
@cli_util.option('--compartment-id', required=True, help="""The OCID of the compartment (remember that the tenancy is simply the root compartment).""")
@cli_util.option('--user-id', required=True, help="""The OCID of the user.""")
@cli_util.option('--group-id', required=True, help="""The OCID of the group.""")
@cli_util.option("--force", is_flag=True, help="Perform removal without prompting for confirmation.")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def remove_user_from_group(ctx, from_json, compartment_id, user_id, group_id, force):
    cli_util.load_context_obj_values_from_defaults(ctx)

    if not force:
        if not click.confirm("Are you sure you want to remove the given user from the given group?"):
            ctx.abort()

    client = cli_util.build_client('identity', ctx)
    memberships = client.list_user_group_memberships(compartment_id=compartment_id, user_id=user_id, group_id=group_id).data

    if memberships and len(memberships) == 1:
        cli_util.render_response(client.remove_user_from_group(user_group_membership_id=memberships[0].id), ctx)
    else:
        sys.exit('User {!r} is not a member of group {!r}'.format(user_id, group_id))


@identity_cli.policy_group.command(name='update', help="""Updates the specified policy. You can update the description or the policy statements themselves.

Policy changes take effect typically within 10 seconds.""")
@cli_util.option('--policy-id', required=True, help="""The OCID of the policy.""")
@cli_util.option('--description', help="""The description you assign to the policy. Does not have to be unique, and it's changeable.""")
@cli_util.option('--statements', help="""A JSON array of policy statements written in the policy language. See [How Policies Work] and [Common Policies]. Example: '["statement 1","statement 2"]' (The single quotes are required.)""")
@cli_util.option('--version-date', help="""The version of the policy. If set to an empty string, when a request comes in for authorization, the policy will be evaluated according to the current behavior of the services at that moment. If set to a particular date (YYYY-MM-DD), the policy will be evaluated according to the behavior of the services on that date.""")
@cli_util.option('--if-match', help="""For optimistic concurrency control. In the PUT or DELETE call for a resource, set the `if-match` parameter to the value of the etag from a previous GET or POST response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help="""Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{\"bar-key\": \"value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help="""Usage of predefined tag keys. These predefined keys are scoped to namespaces. Example: `{\"foo-namespace\": {\"bar-key\": \"foo-value\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@json_skeleton_utils.get_cli_json_input_option({'statements': {'module': 'identity', 'class': 'list[string]'}, 'freeform-tags': {'module': 'identity', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'identity', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'statements': {'module': 'identity', 'class': 'list[string]'}, 'freeform-tags': {'module': 'identity', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'identity', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'identity', 'class': 'Policy'})
@cli_util.wrap_exceptions
def update_policy(ctx, from_json, policy_id, description, statements, version_date, if_match, force, defined_tags, freeform_tags):
    cli_util.load_context_obj_values_from_defaults(ctx)

    client = cli_util.build_client('identity', ctx)
    if statements or version_date:
        if statements is None or version_date is None:
            sys.exit('If updating either statements or version date, both parameters must be specified.')

        if not force:
            result = client.get_policy(policy_id=policy_id)
            etag = result.headers['etag']

            if (if_match and etag != if_match):
                sys.exit('If-match {!r} does not match the current etag, {!r}.'.format(if_match, result.headers['etag']))

            if_match = etag

            existing_statements = cli_util.formatted_flat_dict(result.data.statements)
            if not click.confirm("WARNING: The value passed to statements will overwrite all existing statements for this policy. The existing statements are:\n" + existing_statements + "\nAre you sure you want to continue?"):
                ctx.abort()

    if not force:
        if defined_tags or freeform_tags:
            if not click.confirm("WARNING: Updates to defined-tags and freeform-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    args = {}

    if if_match is not None:
        args['if_match'] = if_match

    details = {}

    if description:
        details['description'] = description
    if statements:
        details['statements'] = cli_util.parse_json_parameter("statements", statements)
    if version_date:
        if len(version_date) == 0:
            version_date = None
        details['versionDate'] = version_date
    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)
    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    result = client.update_policy(policy_id=policy_id, update_policy_details=details, ** args)
    cli_util.render_response(result, ctx)


@cli_util.copy_params_from_generated_command(identity_cli.update_tag, params_to_exclude=['is_retired'])
@identity_cli.tag_group.command(name=cli_util.override('update_tag.command_name', 'update'), help="""Updates the the specified tag""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'identity', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'identity', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'identity', 'class': 'Tag'})
@cli_util.wrap_exceptions
def update_tag_description(ctx, **kwargs):
    ctx.invoke(identity_cli.update_tag, **kwargs)


@identity_cli.tag_group.command(name='retire', short_help='Retire tag and related rules', help="""Retires a tag so that it cannot be used to tag resources. Retiring a tag will also retire the related rules. You can not create a tag with the same name as a retired tag. Tags must be unique within their tag namespace but can be repeated across namespaces. You cannot add a tag with the same name as a retired tag in the same tag namespace.""")
@cli_util.option('--tag-namespace-id', required=True, help="""The OCID of the tag namespace.""")
@cli_util.option('--tag-name', required=True, help="""The name of the tag.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'Tag'})
@cli_util.wrap_exceptions
def retire_tag(ctx, **kwargs):
    tag_namespace_id = kwargs['tag_namespace_id']
    tag_name = kwargs['tag_name']

    if isinstance(tag_namespace_id, six.string_types) and len(tag_namespace_id.strip()) == 0:
        raise click.UsageError('Parameter --tag-namespace-id cannot be whitespace or empty string')

    if isinstance(tag_name, six.string_types) and len(tag_name.strip()) == 0:
        raise click.UsageError('Parameter --tag-name cannot be whitespace or empty string')

    service_kwargs = {}
    details = {'isRetired': True}

    client = cli_util.build_client('identity', ctx)
    result = client.update_tag(
        tag_namespace_id=tag_namespace_id,
        tag_name=tag_name,
        update_tag_details=details,
        **service_kwargs
    )
    cli_util.render_response(result, ctx)


@identity_cli.tag_group.command(name='reactivate', help="""Reactivate tag so it can be used""")
@cli_util.option('--tag-namespace-id', required=True, help="""The OCID of the tag namespace.""")
@cli_util.option('--tag-name', required=True, help="""The name of the tag.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'Tag'})
@cli_util.wrap_exceptions
def reactivate_tag(ctx, **kwargs):
    tag_namespace_id = kwargs['tag_namespace_id']
    tag_name = kwargs['tag_name']

    if isinstance(tag_namespace_id, six.string_types) and len(tag_namespace_id.strip()) == 0:
        raise click.UsageError('Parameter --tag-namespace-id cannot be whitespace or empty string')

    if isinstance(tag_name, six.string_types) and len(tag_name.strip()) == 0:
        raise click.UsageError('Parameter --tag-name cannot be whitespace or empty string')

    service_kwargs = {}
    details = {'isRetired': False}

    client = cli_util.build_client('identity', ctx)
    result = client.update_tag(
        tag_namespace_id=tag_namespace_id,
        tag_name=tag_name,
        update_tag_details=details,
        **service_kwargs
    )
    cli_util.render_response(result, ctx)


@cli_util.copy_params_from_generated_command(identity_cli.update_tag_namespace, params_to_exclude=['is_retired'])
@identity_cli.tag_namespace_group.command(name=cli_util.override('update_tag_namespace.command_name', 'update'), help="""Updates the specified tagNamespace""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'identity', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'identity', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'identity', 'class': 'TagNamespace'})
@cli_util.wrap_exceptions
def update_tag_namespace_description(ctx, **kwargs):
    tag_namespace_id = kwargs['tag_namespace_id']
    description = kwargs.get('description')
    freeform_tags = kwargs.get('freeform_tags')
    defined_tags = kwargs.get('defined_tags')

    if isinstance(tag_namespace_id, six.string_types) and len(tag_namespace_id.strip()) == 0:
        raise click.UsageError('Parameter --tag-namespace-id cannot be whitespace or empty string')

    if not kwargs.get('force'):
        if freeform_tags or defined_tags:
            if not click.confirm("WARNING: Updates to freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    service_kwargs = {}
    details = {}

    if description is not None:
        details['description'] = description

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('identity', ctx)
    result = client.update_tag_namespace(
        tag_namespace_id=tag_namespace_id,
        update_tag_namespace_details=details,
        **service_kwargs
    )
    cli_util.render_response(result, ctx)


@identity_cli.tag_namespace_group.command(name='retire', short_help='Retire namespace and its tags and rules', help="""Retire the namespace, all the contained tags and the related rules. Reactivating a namespace  will not reactivate any tag definition that is retired when the namespace was retired. They will have to be individually reactivated *after* the namespace is reactivated. You can't add a namespace with the same name as a retired namespace in the same tenant.""")
@cli_util.option('--tag-namespace-id', required=True, help="""The OCID of the tag namespace.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'TagNamespace'})
@cli_util.wrap_exceptions
def retire_tag_namespace(ctx, **kwargs):
    tag_namespace_id = kwargs['tag_namespace_id']

    service_kwargs = {}
    details = {'isRetired': True}

    client = cli_util.build_client('identity', ctx)
    result = client.update_tag_namespace(
        tag_namespace_id=tag_namespace_id,
        update_tag_namespace_details=details,
        **service_kwargs
    )
    cli_util.render_response(result, ctx)


@identity_cli.tag_namespace_group.command(name='reactivate', short_help='Reactivate namespace (only)', help="""Reactivates a namespace. Reactivating a namespace will not reactivate any tag definition that is retired when the namespace was retired. They will have to be individually reactivated *after* the namespace is reactivated.""")
@cli_util.option('--tag-namespace-id', required=True, help="""The OCID of the tag namespace.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'TagNamespace'})
@cli_util.wrap_exceptions
def reactivate_tag_namespace(ctx, **kwargs):
    tag_namespace_id = kwargs['tag_namespace_id']

    service_kwargs = {}
    details = {'isRetired': False}

    client = cli_util.build_client('identity', ctx)
    result = client.update_tag_namespace(
        tag_namespace_id=tag_namespace_id,
        update_tag_namespace_details=details,
        **service_kwargs
    )
    cli_util.render_response(result, ctx)


@cli_util.copy_params_from_generated_command(identity_cli.upload_api_key, params_to_exclude=['key'])
@identity_cli.api_key_group.command(name='upload', help=identity_cli.upload_api_key.help)
@cli_util.option('--key', help="""The public key.  Must be an RSA key in PEM format. Either this option or --key-file must be specified""")
@cli_util.option('--key-file', type=click.File('r'), help="""A file containing the public key.  Must be an RSA key in PEM format. Either this option or --key must be specified""")
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'identity', 'class': 'ApiKey'})
@cli_util.wrap_exceptions
def upload_api_key(ctx, **kwargs):
    if not kwargs.get('key') and not kwargs.get('key_file'):
        raise cli_exceptions.RequiredValueNotInDefaultOrUserInputError('Must specify either --key or --key-file.')

    if kwargs.get('key') and kwargs.get('key_file'):
        raise cli_exceptions.RequiredValueNotInDefaultOrUserInputError('Cannot specify both --key and --key-file.')

    key_file = kwargs.get('key_file')
    if key_file:
        kwargs['key'] = key_file.read()

    # remove this since it wont be recognized by identity_cli.upload_api_key
    kwargs.pop('key_file')

    ctx.invoke(identity_cli.upload_api_key, **kwargs)
