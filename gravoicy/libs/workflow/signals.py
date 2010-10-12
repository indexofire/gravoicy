# -*- coding: utf-8 -*-
from django.dispatch import Signal

# Fired when a role is assigned to a user for a particular run of a workflow
# (defined in the WorkflowActivity). The sender is an instance of the
# WorkflowHistory model logging this event.
role_assigned = Signal()
# Fired when a role is removed from a user for a particular run of a workflow
# (defined in the WorkflowActivity). The sender is an instance of the
# WorkflowHistory model logging this event.
role_removed = Signal()
# Fired when a new WorkflowActivity starts navigating a workflow. The sender is
# an instance of the WorkflowActivity model
workflow_started = Signal()
# Fired just before a WorkflowActivity creates a new item in the Workflow History
# (the sender is an instance of the WorkflowHistory model)
workflow_pre_change = Signal()
# Fired after a WorkflowActivity creates a new item in the Workflow History (the
# sender is an instance of the WorkflowHistory model)
workflow_post_change = Signal()
# Fired when a WorkflowActivity causes a transition to a new state (the sender is
# an instance of the WorkflowHistory model)
workflow_transitioned = Signal()
# Fired when some event happens during the life of a WorkflowActivity (the
# sender is an instance of the WorkflowHistory model)
workflow_event_completed = Signal()
# Fired when a comment is created during the lift of a WorkflowActivity (the
# sender is an instance of the WorkflowHistory model)
workflow_commented = Signal()
# Fired when an active WorkflowActivity reaches a workflow's end state. The
# sender is an instance of the WorkflowActivity model
workflow_ended = Signal()
