# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
import re
import space as space

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to TechVillage. "
                        f"My name is Tamara. "
                    )
                )
                await self.services_offered(turn_context)
 

    async def services_offered(self, turn_context: TurnContext):

        response = MessageFactory.text("Here we are offering the following Services: ")

        response.suggested_actions = SuggestedActions(
            actions=[
                CardAction(title="1. Space", type=ActionTypes.im_back, value="space"),
                CardAction(title="2. Community", type=ActionTypes.im_back, value="community"),
                CardAction(title="3. Inquiries", type=ActionTypes.im_back, value="inquires")
            ]
        )
        return await turn_context.send_activity(response)


    async def space_services(self, turn_context: TurnContext):
        basic_space = space.basic_space()  
        await turn_context.send_activity('For Co-Working Spaces the following is available: \n 1. %s which costs %s' % (str(basic_space['title']), str(basic_space['cost'])))  
        return await self.services_offered(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        user_response = turn_context.activity.text.lower
        if user_response is 'space':
            await turn_context.send_activity(f'This is our space, What do you want to know about our space?')
        
        return await self.space_services(turn_context)