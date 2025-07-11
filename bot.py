import interactions
import json

bot = interactions.Client(token="")

@bot.command(
    name="secret_santa",
    description="Little minion for the Secret Santa",
    scope=[1037255693285216367, 952698433087614987],
)
async def secret_santa(ctx: interactions.CommandContext):
    pass
 
@secret_santa.subcommand()
async def join(ctx: interactions.CommandContext):
    """Join the fun for a Merry Christmas with your best friendos"""
    with open(file="names.json", mode="r") as file:
        ids = json.loads(file.read())

    if (ctx.author.id in ids["ids"]):
        await ctx.send("```You are already on the list buddy.```", ephemeral=True)
        return

    if (ctx.author.id not in ids["ids"]):
        ids["ids"].append(int(ctx.author.id))

    img = interactions.EmbedImageStruct(
        url="https://images.nightcafe.studio/jobs/kiGSTyU7VIfPtr6CalSe/kiGSTyU7VIfPtr6CalSe--1--n5fi2_2x-real-esrgan-x4-plus.jpg?tr=w-1600,c-at_max",
    )

    embed = interactions.Embed(
        title="Secret Santa",
        description="Hey dude, thanks for siging up, you're now on the list. \n You will be assigned a random person and you must buy a present for them. The budget for presents is **$20NZD**.\nAny shipping or processing costs are not included in the budget (so if something is $20 with $15 shipping, it's fine) \n \nYour secret santa will be revealed <t:1734087540:R> \n Please be patient and Merry Christmas my loves <3 \n\nps: date, time and location of actual gathering to give gifts is tbc",
        image = img
    )

    with open(file="names.json", mode="w") as file:
        file.write(json.dumps(ids))

    message = await ctx.author.send(embeds=embed)

    await ctx.send("**Check yours DMs!** \n *Jump to message:* https://discord.com/channels/@me/"+str(message.channel_id)+"/"+str(message.id)+"", ephemeral=True)
    return

@secret_santa.subcommand()
async def list(ctx: interactions.CommandContext):
    """List out everyone who is already joined up to the fun."""
    file = open(file="names.json", mode="r")
    ids = json.loads(file.read())
    embed = interactions.Embed(
        title="Secret Santa",
        description="Thank you again to everyone who has signed up!",
    )
    for i in ids["ids"]:
        username = await interactions.get(bot, interactions.Member, parent_id=ctx.guild_id, object_id=i)
        embed.add_field(name=username.name, value=" ")

    await ctx.send(embeds=embed, ephemeral=True)
    return

@bot.command(
    name="wishlist",
    description="See a person's wishlist or add to your own",
    scope=[1037255693285216367, 952698433087614987],
)
async def wishlist(ctx: interactions.CommandContext):
    pass

@wishlist.subcommand(
    options = [
        interactions.Option(
            name="user",
            description="Search someone's wishlist",
            type=interactions.OptionType.USER,
            required=True,
        ),
    ],
)
async def search(ctx: interactions.CommandContext, user: interactions.Member):
    """Search for someone's wishlist and view what they might want."""
    with open(file="names.json", mode="r") as file:
        data = json.loads(file.read())

    if ctx.author.id not in data["ids"]:
        await ctx.send("**Please sign up to the Secret Santa first with /secret_santa join!**", ephemeral=True)
        return
    
    if user.id not in data["ids"]:
        await ctx.send("**This user was not found in the Secret Santa database...**", ephemeral=True)
        return
    
    if f"{user.id}" not in data["wishlists"]:
        await ctx.send(f"*{user.name} is yet to add to their wishlist...*", ephemeral=True)
        return

    if len(data["wishlists"][f"{user.id}"]) < 1:
        await ctx.send(f"*{user.name} is yet to add to their wishlist...*", ephemeral=True)
        return
    
    message = f"**{user.name}**'s wishlist. \n"
    for it in data["wishlists"][f"{user.id}"]:
        message += f"\n{it}"

    await ctx.send(message, ephemeral=True)
    return

@wishlist.subcommand(
    options = [
        interactions.Option(
            name="item",
            description="Add to your wishlist",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def add(ctx: interactions.CommandContext, item: str):
    """Let others know what you may want to get so they can have an idea! (Lazy fucks)"""

    with open(file="names.json", mode="r") as file:
        data = json.loads(file.read())

    if ctx.author.id not in data["ids"]:
        await ctx.send("**Please sign up to the Secret Santa first with /secret_santa join!**", ephemeral=True)
        return

    if f"{ctx.author.id}" not in data["wishlists"]:
        data["wishlists"][f"{ctx.author.id}"] = []
    
    data["wishlists"][f"{ctx.author.id}"].append(f"{item}")

    with open(file="names.json", mode="w") as file:
        file.write(json.dumps(data))

    message = f"You have just added **{item}** to your wishlist. \n\nYour full wishlist is now:"
    for it in data["wishlists"][f"{ctx.author.id}"]:
        message += f"\n{it}"

    await ctx.send(message, ephemeral=True)
    return

@wishlist.subcommand(
    options = [
        interactions.Option(
            name="item",
            description="Remove from your wishlist",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def remove(ctx: interactions.CommandContext, item: str):
    """Let others know what you may want to get so they can have an idea! (Lazy fucks)"""

    with open(file="names.json", mode="r") as file:
        data = json.loads(file.read())

    if ctx.author.id not in data["ids"]:
        await ctx.send("**Please sign up to the Secret Santa first with /secret_santa join!**", ephemeral=True)
        return

    if len(data["wishlists"][f"{ctx.author.id}"]) < 1:
        await ctx.send("**Wishlist is empty...**", ephemeral=True)
        return

    if f"{ctx.author.id}" not in data["wishlists"]:
        await ctx.send("**Wishlist is empty...**", ephemeral=True)
        return

    if item not in data["wishlists"][f"{ctx.author.id}"]:
        await ctx.send("**Item not on wishlist...**", ephemeral=True)
        return

    data["wishlists"][f"{ctx.author.id}"].remove(item)

    with open(file="names.json", mode="w") as file:
        file.write(json.dumps(data))
    
    message = f"You have just removed **{item}** from your wishlist. \n\nYour full wishlist is now:"

    if len(data["wishlists"][f"{ctx.author.id}"]) < 1:
        message = f"You have just removed **{item}** from your wishlist. \n\n*Your full wishlist is now empty*"

    else: 
        for it in data["wishlists"][f"{ctx.author.id}"]:
            message += f"\n{it}"

    await ctx.send(message, ephemeral=True)
    return

# @bot.command(
#     name="dothething",
#     description="does the thing",
#     scope=[1037255693285216367, 952698433087614987],
# )
# async def dothething(ctx: interactions.CommandContext):

#     with open(file="names.json", mode="r") as file:
#         data = json.loads(file.read())
 
#     img = interactions.EmbedImageStruct(
#         url="https://images.nightcafe.studio/jobs/kiGSTyU7VIfPtr6CalSe/kiGSTyU7VIfPtr6CalSe--1--n5fi2_2x-real-esrgan-x4-plus.jpg?tr=w-1600,c-at_max",
#     )

#     for name in data["ids"]:
        
#         secret_santa = await interactions.get(bot, interactions.Member, parent_id=ctx.guild_id, object_id=data["santas"][f"{name}"])
#         secret_santa = secret_santa.name

#         embed = interactions.Embed(
#             title="Secret Santa",
#             description=f"Hey, I finally did it!\n\nHere is your secret santa!\n\nThe person you have to get a gift for is...***{secret_santa}***\n\nYou can use the bot to look up their wishlist (if they have one).\n*If the bot isn't on please let me know so I can put it on for you.*\n\nThe exchange of presents will be done on <t:1736571600:F> at **Tom's house @ 58 Rex Street Miramar.**\nBring drinks n food n shit let's get litty after!",
#             image = img
#         )

#         username = await interactions.get(bot, interactions.Member, parent_id=ctx.guild_id, object_id=name)

#         await username.send(embeds=embed)

#         print(f"{name} done")



print("Bot online!")

bot.start()