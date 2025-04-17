import disnake
from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
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
        

def setup(bot):
    bot.add_cog(General(bot))
