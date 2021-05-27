class Reader(object):
    """docstring for Reader"""
    def __init__(self):
        super(Reader, self).__init__()
        self.cmds = {}
        self.not_in_cmds = ""
        self.not_enougth_arg = ""
        self.not_in_private = ""
        self.forbidden_channel = ""
        
    """
    It read a string command and execute it, if it returns somthing, it will return it AND print it
    msg_discord is eventualy used if the funciton needs additional informations about the message.
    levels are level object for Metis to use
    """
    def read(self, string,msg_discord,levels):
        sliced_str = string.split()
        if len(sliced_str) != 0 and sliced_str[0] in self.cmds:
            sliced_str = custom_split(string, " ", self.cmds[sliced_str[0]][1]+1)
            args_need = sliced_str[1:1+self.cmds[sliced_str[0]][1]]
            args_supp = sliced_str[self.cmds[sliced_str[0]][1]+1:]
            if not self.cmds[sliced_str[0]][3] and text.channel.type == discord.ChannelType.private:
                return self.not_in_private
            if msg_discord.channel.category_id in self.cmds[sliced_str[0]][5] or msg_discord.channel.category_id in self.cmds[sliced_str[0]][4] :
                return self.forbidden_channel
            if len(args_need) < self.cmds[sliced_str[0]][1]:
                return self.not_enougth_arg
            if not self.cmds[sliced_str[0]][2]:
                return self.cmds[sliced_str[0]][0](args_need,args_supp,msg_discord,levels)
            else :
                txt = ""
                for x in args_supp:
                    txt += " " + x
                return self.cmds[sliced_str[0]][0](args_need,txt[1:],msg_discord,levels)
        elif self.not_in_cmds != "":
            #print(self.not_in_cmds)
            return self.not_in_cmds
        else :
            #print("This is not a command.")
            return "This is not a command."

    """
    It add a cmd to cmds
    cmd added to cmds MUST have the following form : 
    cmd([must_arg_list], followed_string OR [followed_arg_list],msg_discord,levels)
    func is a function / args_min is a number / is_text is a boolean
    """
    def add_cmds(self, name, func, args_min, is_text, can_private, forbidden_channel, forbidden_catergory):
        if " " in name:
            print("Error Reader.add_cmds, name should not contain spaces")
        else :
            self.cmds[name] = (func,args_min,is_text, can_private, forbidden_channel, forbidden_catergory)


"""
A custum split to help building a split with multiple spaces
"""
def custom_split(string, ch, num):
    return_v = [""]
    i = 0
    while i < len(string) and (string[i] != " " or return_v[len(return_v)-1] == "" or len(return_v) != num):
        if string[i] != " ":
            return_v[len(return_v)-1] += string[i]
        elif return_v[len(return_v)-1] != "":
            return_v.append("")
        i += 1
    return_v.append(string[i+1:])
    return return_v