from colorclass import Color, list_tags
print(Color(f"{{red}}thing what{{/red}}"))
# print(Color('{red}Sample Text{/red}', keep_tags=True))
# for val in list_tags():
#     print(Color(f"{val[0]}: {{{val[0]}}}{val[0]}{{{val[1]}}}"))



type IPA = str #> custom type for IPA
type span = tuple[int,int]

def colorprint(*values:object,
    sep: str | None = " ",
    end: str | None = "\n"):
    # thing = []
    for val in values:
        print(Color(val),end=sep, sep="")
    print(end,end="",sep="")


# colorprint("{red}thing what{/red}","{green}Sample Text{/green}")


def say_span(span:span):
    return f"({span[0]},{span[1]})"