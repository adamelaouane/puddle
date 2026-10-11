from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch

from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage
from django.db.models import Count

@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    # Prevent users from messaging themselves
    if item.created_by == request.user:
        return redirect('dashboard:index')

    # Check whether a conversation already exists between the user and the product owner
    conversation = (
        Conversation.objects
        .filter(item=item, members=request.user)
        .filter(members=item.created_by)
        .annotate(member_count=Count('members', distinct=True))
        .filter(member_count=2)
        .first()
    )

    if conversation:
        return redirect('conversation:detail', pk=conversation.pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user, item.created_by)

            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            # Update the conversation's last activity timestamp
            conversation.save()

            return redirect('conversation:detail', pk=conversation.pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item,
    })


@login_required
def inbox(request):
    conversations = (
        Conversation.objects
        .filter(members=request.user)
        .select_related('item')
        .prefetch_related(
            'members',
            Prefetch(
                'message',
                queryset=ConversationMessage.objects
                .select_related('created_by')
                .order_by('-created_at'),
                to_attr='messages_by_latest'
            )
        )
        .distinct()
        .order_by('-modified_at')
    )

    for conversation in conversations:
        messages = conversation.messages_by_latest

        # Get the latest message in the conversation
        conversation.last_message = messages[0] if messages else None

        # Count unread messages for the current user
        conversation.unread_count = (
            conversation.message
            .exclude(created_by=request.user)
            .exclude(read_by=request.user)
            .count()
        )

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


@login_required
def detail(request, pk):
    # Ensure that the current user is a member of the conversation
    conversation = get_object_or_404(
        Conversation,
        pk=pk,
        members=request.user
    )

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            # Mark the sender's message as read
            message.read_by.add(request.user)

            # Update the conversation's last activity timestamp
            conversation.save()

            return redirect('conversation:detail', pk=conversation.pk)
    else:
        form = ConversationMessageForm()

    # Mark messages from other users as read
    conversation.message.exclude(
        created_by=request.user
    ).exclude(
        read_by=request.user
    ).update() if False else None

    for message in conversation.message.exclude(created_by=request.user):
        message.read_by.add(request.user)

    # Retrieve all messages in chronological order
    messages = (
        conversation.message
        .select_related('created_by')
        .order_by('created_at')
    )

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form,
        'messages': messages,
    })