import disnake
from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# 👨‍🦰 Пользователь
    @commands.slash_command(name="пользователь")
    async def user(self, inter: disnake.ApplicationCommandInteraction):
        pass
    
    @user.sub_command(name="аватар", description="Показать аватар пользователя.")
    async def user_avatar(self, inter: disnake.ApplicationCommandInteraction, 
                          пользователь: disnake.Member = commands.Param(default=None, 
                                                                        description="Выберите пользователя.")
                          ):
        target = пользователь or inter.author
        
        user_avatar = disnake.Embed(title=f"Аватар {target.name}", color=0x5865f1)
        user_avatar.set_image(url=target.display_avatar.url)
        
        await inter.response.send_message(embed=user_avatar, ephemeral=True)
    

#🪐 Сервер
    @commands.slash_command(name="сервер")
    async def server_manager(self, inter: disnake.ApplicationCommandInteraction):
        pass
    
    @server_manager.sub_command(name="информация", description="Информация о сервере.")
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        
        timestamp = int(inter.guild.created_at.timestamp())
        
        embed = disnake.Embed(color=0x5865f1)
        embed.set_author(name=f"Информация о {inter.guild.name}", icon_url=inter.guild.icon)
        embed.set_thumbnail(url=inter.guild.icon.url if inter.guild.icon else disnake.Embed.Empty)
        
        embed.add_field(
            name="Владелец:",
            value=f"<:OWNER:1362561676213354606> {inter.guild.owner.mention}",
            inline=True
        )
        
        embed.add_field(
            name="ID:",
            value=f"<:SERVER:1362562819425308672> `{inter.guild.id}`",
            inline=True
        )
        
        embed.add_field(
            name="Создан:",
            value=f"<:CREATED:1362564229571285175> <t:{timestamp}:F> (<t:{timestamp}:R>)",
            inline=False
        )
        
        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(General(bot))
