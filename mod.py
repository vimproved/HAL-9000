async def ban(args, bot, channel, message):
    await user = bot.getUser(int(args[2:-2]))
    banroleids = [738456842707140700, 742128809129803806, 742128992286670910, 742129191277035590]
    userbanroles = []
    for x in user.roles:
        if x.id in banroleids:
            userbanroles.append(x)
    x = userbanroles[-1]
    if x != 3:
        await user.add_roles(banroleids.index(x) + 1)
    else:
        await channel.send("That user is already the highest banned level.")
cmds = {"ban": ('"Bans" the user.', ban)}
desc = "Moderation related commands."
