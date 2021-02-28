
# Library includes

import discord
from discord.ext import commands


class MyHelp(commands.HelpCommand):

    def get_command_signature(self, command: commands.Command):

        short_description: str = command.brief if command.brief != 'None' else 'Brief missing!'

        return_val: str = "`{}{}`: {}".format(
            self.clean_prefix,
            command.qualified_name,
            short_description
        )

        return return_val

    def get_group_signature(self, group: commands.Group):
        return_val: str = "`{}{}`: {}".format(
            self.clean_prefix,
            group.qualified_name,
            group.brief
        )

        for sub_command in group.commands:
            return_val += f"\n ╘ `{sub_command.name}`: {sub_command.brief}"

        return return_val

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help",
            colour=discord.Color.dark_gold()
        )

        embed.set_thumbnail(url=self.context.bot.user.avatar_url)

        for cog, elements in mapping.items():

            fields = []
            elements = await self.filter_commands(elements, sort=True)
            for el in elements:
                if type(el) is commands.Command:
                    fields.append(self.get_command_signature(el))
                elif type(el) is commands.Group:
                    fields.append(self.get_group_signature(el))

            if fields:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(
                    fields), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
