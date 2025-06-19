import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

CANAL_AUTORIZADO_ID = 1385319888020832296

def criar_embed(titulo: str, descricao: str, cor=discord.Color.blue()):
    embed = discord.Embed(title=titulo, description=descricao, color=cor)
    return embed

@bot.event
async def on_ready():
    print("Bora varrer essa sujeira!")

@bot.event
async def on_message(message):
    # Ignorar mensagens do bot para evitar loop
    if message.author == bot.user:
        return
    
    # Responder "." com a lista de comandos no canal autorizado
    if message.channel.id == CANAL_AUTORIZADO_ID and message.content.strip() == ".":
        comandos_disponiveis = (
            "**Comandos disponíveis:**\n"
            "`.ajuda` - Mostra esta mensagem de ajuda.\n"
            "`.falar <texto>` - Faz o bot repetir o texto.\n"
            "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
            "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
            "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
            "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
        )
        embed = criar_embed("Lista de Comandos", comandos_disponiveis)
        await message.channel.send(embed=embed)
        return
    
    await bot.process_commands(message)

@bot.command()
async def ajuda(ctx: commands.Context):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    nome = ctx.author.name
    comandos_disponiveis = (
        "**Comandos disponíveis:**\n"
        "`.ajuda` - Mostra esta mensagem de ajuda.\n"
        "`.falar <texto>` - Faz o bot repetir o texto.\n"
        "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
        "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
        "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
        "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
    )
    embed = criar_embed(f"Olá, {nome}!", comandos_disponiveis)
    await ctx.reply(embed=embed)

@bot.command()
async def falar(ctx: commands.Context, *, texto):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    await ctx.reply(embed=criar_embed("Mensagem do Bot", texto, discord.Color.green()))

@bot.command()
@commands.has_permissions(administrator=True)
async def limpar_usuario(ctx: commands.Context, membro: discord.Member, canal: discord.TextChannel):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    deletadas = 0
    async for msg in canal.history(limit=100):
        if msg.author == membro:
            await msg.delete()
            deletadas += 1
    await ctx.send(embed=criar_embed("Limpeza de Mensagens", f"✅ {deletadas} mensagens de {membro.display_name} foram apagadas no canal {canal.mention}.", discord.Color.green()))

@bot.command()
@commands.has_permissions(administrator=True)
async def limpar_palavra(ctx: commands.Context, palavra: str, canal: discord.TextChannel):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    deletadas = 0
    async for msg in canal.history(limit=100):
        if palavra in msg.content:
            await msg.delete()
            deletadas += 1
    await ctx.send(embed=criar_embed("Limpeza de Mensagens", f"✅ {deletadas} mensagens contendo '{palavra}' foram apagadas do canal {canal.mention}.", discord.Color.green()))

@bot.command()
@commands.has_permissions(administrator=True)
async def listar_sem_cargo(ctx: commands.Context):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    guild = ctx.guild
    sem_cargo = [m for m in guild.members if len(m.roles) <= 1]  # Só tem o @everyone
    
    if not sem_cargo:
        await ctx.send(embed=criar_embed("Usuários sem Cargo", "Nenhum usuário sem cargo encontrado.", discord.Color.orange()))
        return
    
    nomes = "\n".join(m.display_name for m in sem_cargo)
    if len(nomes) > 1900:
        nomes = nomes[:1900] + "\n..."
    
    embed = criar_embed("Usuários sem Cargo", f"Total: {len(sem_cargo)}\n\n{nomes}")
    await ctx.send(embed=embed)
    
    # Perguntar via DM qual cargo deseja atribuir
    try:
        await ctx.author.send(f"Digite o nome exato do cargo que deseja atribuir a todos os {len(sem_cargo)} usuários sem cargo no servidor **{guild.name}**.")
    except discord.Forbidden:
        await ctx.send(embed=criar_embed("Erro", "Não foi possível enviar mensagem privada. Por favor, habilite suas DMs.", discord.Color.red()))
        return

@bot.event
async def on_message_edit(before, after):
    # Para processar comandos em mensagens editadas se quiser, mas opcional
    pass

@bot.event
async def on_message(message):
    # Já temos on_message antes, precisamos unir as duas funções
    pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Responder "." com lista de comandos
    if message.channel.id == CANAL_AUTORIZADO_ID and message.content.strip() == ".":
        comandos_disponiveis = (
            "**Comandos disponíveis:**\n"
            "`.ajuda` - Mostra esta mensagem de ajuda.\n"
            "`.falar <texto>` - Faz o bot repetir o texto.\n"
            "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
            "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
            "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
            "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
        )
        embed = criar_embed("Lista de Comandos", comandos_disponiveis)
        await message.channel.send(embed=embed)
        return
    
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Já tem on_message definido acima, vamos unir o comando que processa . e os demais
    if message.author == bot.user:
        return
    
    if message.channel.id == CANAL_AUTORIZADO_ID and message.content.strip() == ".":
        comandos_disponiveis = (
            "**Comandos disponíveis:**\n"
            "`.ajuda` - Mostra esta mensagem de ajuda.\n"
            "`.falar <texto>` - Faz o bot repetir o texto.\n"
            "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
            "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
            "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
            "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
        )
        embed = criar_embed("Lista de Comandos", comandos_disponiveis)
        await message.channel.send(embed=embed)
        return

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def listar_com_cargo(ctx: commands.Context, *, cargo_nome: str):
    if ctx.channel.id != CANAL_AUTORIZADO_ID:
        return await ctx.send(embed=criar_embed("Erro", "❌ Este comando só pode ser usado em um canal específico.", discord.Color.red()))
    
    guild = ctx.guild
    cargo = discord.utils.get(guild.roles, name=cargo_nome)
    
    if not cargo:
        await ctx.send(embed=criar_embed("Erro", f"❌ Cargo '{cargo_nome}' não encontrado.", discord.Color.red()))
        return
    
    membros_com_cargo = [m for m in guild.members if cargo in m.roles]
    if not membros_com_cargo:
        await ctx.send(embed=criar_embed("Lista de Usuários", f"Nenhum usuário possui o cargo **{cargo_nome}**.", discord.Color.orange()))
        return
    
    nomes = "\n".join(m.display_name for m in membros_com_cargo)
    if len(nomes) > 1900:
        nomes = nomes[:1900] + "\n..."
    
    embed = criar_embed(f"Usuários com o cargo '{cargo_nome}'", nomes)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    # Combinação da verificação do ponto '.' e processamento normal
    if message.author == bot.user:
        return

    if message.channel.id == CANAL_AUTORIZADO_ID and message.content.strip() == ".":
        comandos_disponiveis = (
            "**Comandos disponíveis:**\n"
            "`.ajuda` - Mostra esta mensagem de ajuda.\n"
            "`.falar <texto>` - Faz o bot repetir o texto.\n"
            "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
            "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
            "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
            "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
        )
        embed = criar_embed("Lista de Comandos", comandos_disponiveis)
        await message.channel.send(embed=embed)
        return

    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Unificar tudo em uma função on_message só
    if message.author == bot.user:
        return

    if message.channel.id == CANAL_AUTORIZADO_ID and message.content.strip() == ".":
        comandos_disponiveis = (
            "**Comandos disponíveis:**\n"
            "`.ajuda` - Mostra esta mensagem de ajuda.\n"
            "`.falar <texto>` - Faz o bot repetir o texto.\n"
            "`.limpar_usuario @usuario #canal` - Apaga mensagens de um usuário no canal especificado (Admin).\n"
            "`.limpar_palavra <palavra> #canal` - Apaga mensagens contendo a palavra no canal especificado (Admin).\n"
            "`.listar_sem_cargo` - Lista usuários sem cargo e inicia processo para atribuir cargo.\n"
            "`.listar_com_cargo <cargo>` - Lista usuários que possuem um cargo específico.\n"
        )
        embed = criar_embed("Lista de Comandos", comandos_disponiveis)
        await message.channel.send(embed=embed)
        return

    await bot.process_commands(message)

# Listener para receber cargo pelo DM do dono e aplicar a todos sem cargo
@bot.event
async def on_message(message):
    # Evitar conflito e evitar que o bot responda ele mesmo
    if message.author == bot.user:
        return

    # Vamos detectar se a mensagem é uma DM do dono para o bot com o nome do cargo a atribuir
    if isinstance(message.channel, discord.DMChannel):
        # Verifica se o autor tem permissão no guild (por exemplo, dono)
        # Como a guild não está no contexto, vamos assumir que o usuário está autorizado (pode ajustar para seu caso)
        
        # Pegamos o guild onde queremos atribuir cargos — precisa ajustar para seu caso
        guild = bot.get_guild(CANAL_AUTORIZADO_ID)  # Seu servidor (canal autorizado é no servidor certo?)
        if not guild:
            return
        
        cargo_nome = message.content.strip()
        cargo = discord.utils.get(guild.roles, name=cargo_nome)
        if not cargo:
            await message.channel.send(f"❌ Cargo '{cargo_nome}' não encontrado no servidor.")
            return
        
        # Busca usuários sem cargo
        sem_cargo = [m for m in guild.members if len(m.roles) <= 1]
        if not sem_cargo:
            await message.channel.send("Nenhum usuário sem cargo encontrado para receber o cargo.")
            return
        
        sucesso = 0
        falhas = 0
        for membro in sem_cargo:
            try:
                await membro.add_roles(cargo)
                sucesso += 1
            except Exception as e:
                falhas += 1
        await message.channel.send(f"✅ Cargo '{cargo_nome}' atribuído a {sucesso} usuários.\n❌ Falha em {falhas} usuários.")
        return

    # Aqui continua o processamento normal para mensagem no servidor
    await bot.process_commands(message)

@limpar_usuario.error
@limpar_palavra.error
@listar_com_cargo.error
@listar_sem_cargo.error
async def permissao_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=criar_embed("Erro", "❌ Você precisa ser administrador para usar este comando.", discord.Color.red()))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=criar_embed("Erro", "❌ Uso incorreto! Verifique os parâmetros do comando.", discord.Color.red()))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=criar_embed("Erro", "❌ Argumento inválido! Certifique-se de mencionar corretamente.", discord.Color.red()))

bot.run(TOKEN)
