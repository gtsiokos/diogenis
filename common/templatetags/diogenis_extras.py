from django import template

register = template.Library()

# Copyright 2009, EveryBlock
# This code is released under the GPL.
def raw(parser, token):
    # Whatever is between {% raw %} and {% endraw %} will be preserved as
    # raw, unrendered template code.
    text = []
    parse_until = 'endraw'
    tag_mapping = {
        template.TOKEN_TEXT: ('', ''),
        template.TOKEN_VAR: ('{{', '}}'),
        template.TOKEN_BLOCK: ('{%', '%}'),
        template.TOKEN_COMMENT: ('{#', '#}'),
    }
    # By the time this template tag is called, the template system has already
    # lexed the template into tokens. Here, we loop over the tokens until
    # {% endraw %} and parse them to TextNodes. We have to add the start and
    # end bits (e.g. "{{" for variables) because those have already been
    # stripped off in a previous part of the template-parsing process.
    while parser.tokens:
        token = parser.next_token()
        if token.token_type == template.TOKEN_BLOCK and token.contents == parse_until:
            return template.TextNode(u''.join(text))
        start, end = tag_mapping[token.token_type]
        text.append(u'%s%s%s' % (start, token.contents, end))
    parser.unclosed_block_tag(parse_until)

raw = register.tag(raw)

@register.filter(name='truncatechars')
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of letters

    Argument: Number of letters to truncate after
    """
    def truncate_chars(s, num):
        "Truncates a string after a certain number of letters."
        length = int(num)
        letters = [l for l in s]
        if len(letters) > length:
            letters = letters[:length]
            if not letters[-3:] == ['.','.','.']:
                letters += ['.','.','.']
        return ''.join(letters)

    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently
    if not isinstance(value, basestring):
        value = str(value)
    return truncate_chars(value, length)
