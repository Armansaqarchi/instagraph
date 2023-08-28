

class IsChatMemberPermission:

    def check_object_permission(self, user, obj):

        if not user.is_authenticated or not obj:
            return False

        if user.is_superuser:
            return True

        account = user.account
        if obj.chat_type == "PRIVATE_CHAT":
            private_chat = obj.privatechat
            if account in [private_chat.member1, private_chat.member2]:
                return True

        elif obj.chat_type == "GROUP_CHAT":
            group_chat = obj.groupchat
            if account in group_chat.accounts:
                return True
        print("two")

        return False







