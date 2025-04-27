import disnake
from disnake.ext import commands
import config
import datetime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="мут")
    async def mute_manager(self, inter: disnake.ApplicationCommandInteraction):
        pass
    
    @mute_manager.sub_command(name="выдать", description="Выдать мут пользователю.")
    async def give_mute(self, inter: disnake.ApplicationCommandInteraction, 
                        пользователь: disnake.Member = commands.Param(description="Укажите пользователя."),
                        длительность: str = commands.Param(description="Выберите длительность.", 
                                                           choices=[
                                                                "5 минут","10 минут", "20 минут", "30 минут", "1 час",  "2 часа"
                                                                ]),
                        причина: str = commands.Param(description="Выберите причину.", 
                                                      choices=[
                                                          "Флуд", "Нарушение правил сервера"
                                                      ])
                        ):
        
        if пользователь.bot:
            return await inter.response.send_message("Ошибка: Я не могу мутить ботов.", ephemeral=True)
        
        if config.MODERATION_ROLE not in [role.id for role in inter.author.roles]:
            return await inter.response.send_message("Ошибка: Вы не являетесь модерацией сервера.", ephemeral=True)
        
        if пользователь.id == inter.author.id:
            return await inter.response.send_message("Ошибка: Вы не можете замутить самого себя.", ephemeral=True)
        
        if пользователь.top_role.position >= inter.author.top_role.position:
            return await inter.response.send_message("Ошибка: Невозможно выдать мут пользователю с равной или более высокой ролью.", ephemeral=True)
        
        duration_mapping = {
            "5 минут": datetime.timedelta(minutes=5),
            "10 минут": datetime.timedelta(minutes=10),
            "20 минут": datetime.timedelta(minutes=20),
            "30 минут": datetime.timedelta(minutes=30),
            "1 час": datetime.timedelta(hours=1),
            "2 часа": datetime.timedelta(hours=2),
        }
        
        mute_duration = duration_mapping.get(длительность)
        if mute_duration is None:
            return await inter.response.send_message("Ошибка: неверная длительность мута.", ephemeral=True)
        
        try:
            await пользователь.timeout(duration=mute_duration, reason=причина)
        except disnake.Forbidden:
            return await inter.response.send_message("Ошибка: У меня недостаточно прав для выдачи мута этому пользователю.", ephemeral=True)
        
        embed = disnake.Embed(color=disnake.Color.blurple(), description=
                              f"{пользователь.mention} отправлен в тайм-аут\n"
                              f"Длительность: {длительность}\n"
                              f"Причина: {причина}\n"
                              f"Модератор: {inter.author.mention}"
            )
        embed.set_author(name=пользователь.name, icon_url=пользователь.display_avatar.url)
        await inter.response.send_message(embed=embed)
        original_message = await inter.original_message()
        await original_message.add_reaction("✅")
        

def setup(bot):
    bot.add_cog(Moderation(bot))
