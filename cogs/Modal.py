import disnake
from disnake.ext import commands
from Database.Database import Database


class RecruitModal(disnake.ui.Modal):
    def __init__(self):
        self.db = Database()
        
        components = [
            disnake.ui.TextInput(label="Имя", placeholder="Введите имя", custom_id="name"),
            disnake.ui.TextInput(label="Никнейм", placeholder="Введите никнейм", custom_id="nickname"),
            disnake.ui.TextInput(label="Возраст", placeholder="Введите возраст", custom_id="age", max_length=2),
            disnake.ui.TextInput(label="Почему хотите занять должность?", placeholder="Введите ответ", custom_id="info"),
        ]
        
        super().__init__(title="Заявка на Офицера", components=components, custom_id="recruit_modal")
        
    async def callback(self, inter: disnake.ModalInteraction):
        user_id = inter.author.id
        name = inter.text_values["name"]
        nickname = inter.text_values["nickname"]
        age = inter.text_values["age"]
        info = inter.text_values["info"]
        
        if not age.isdigit():
            error_embed = disnake.Embed(color=disnake.Color.blurple(), description="Возраст должен быть числом!")
            error_embed.set_author(name="Ошибка", icon_url=inter.author.display_avatar.url)
            await inter.response.send_message(embed=error_embed, ephemeral=True)
            return
        
        recruit_exists = self.db.check_recruit_exists(user_id, status="Waiting")
        if recruit_exists:
            error_embed = disnake.Embed(color=disnake.Color.blurple(), description="У вас уже есть активная заявка.")
            error_embed.set_author(name="Ошибка", icon_url=inter.author.display_avatar.url)
            await inter.response.send_message(embed=error_embed, ephemeral=True)
            return


        success_embed = disnake.Embed(color=disnake.Color.blurple(), description="Ваша заявка была отправлена на рассмотрение Администрации.")
        success_embed.set_author(name="Отправлено", icon_url=inter.author.display_avatar.url)
        await inter.response.send_message(embed=success_embed, ephemeral=True)
        
        channel = inter.guild.get_channel(1363307461829853414)
        
        adm_embed = disnake.Embed(color=disnake.Color.blurple())
        adm_embed.set_author(name=inter.author.name, icon_url=inter.author.display_avatar.url)
        adm_embed.add_field(name="", value=name, inline=False)
        adm_embed.add_field(name="", value=nickname, inline=False)
        adm_embed.add_field(name="", value=age, inline=False)
        adm_embed.add_field(name="", value=info, inline=False)
        message = await channel.send(embed=adm_embed)
        message_id = message.id
        
        try:
            self.db.add_recruit(message_id, user_id, nickname, name, age, info, status="Waiting")
        except Exception as e:
            await inter.followup.send("Произошла ошибка при добавлении заявки в базу данных.", ephemeral=True)


 
class RecruitSelect(disnake.ui.Select):
    def __init__(self):
        
        options = [
            disnake.SelectOption(label="Офицер", value="Офицер", description="Подать заявку на Офицера гильдии."),
        ]
        
        super().__init__(placeholder="Выберите пункт", options=options, custom_id="recruit_select", min_values=0, max_values=1)
        
    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.send_modal(RecruitModal())
        
        
class RecruitCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
        
    @commands.command()
    async def recruit(self, ctx):
        view = disnake.ui.View()
        view.add_item(RecruitSelect())
        await ctx.send(view=view)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.persistent_views_added:
            return
    
        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitSelect())
        self.bot.add_view(view=view, message_id=1363329207685615846)


def setup(bot):
    bot.add_cog(RecruitCommands(bot))
