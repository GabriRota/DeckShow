from django import template

register = template.Library()

@register.filter
def condition_emoji(conditions):
    emoji_color = {
        'Mint': ('fa-face-laugh-beam fa-lg', '#7142ff'),
        'Near mint': ('fa-face-grin-beam fa-lg', '#00c48c'),  
        'Excellent': ('fa-face-grin fa-lg', '#a8e100'),       
        'Good': ('fa-face-smile fa-lg', '#FFD43B'),          
        'Light played': ('fa-face-meh fa-lg', '#ffae00'),    
        'Played': ('fa-face-frown fa-lg', '#ff5000'),       
        'Poor': ('fa-face-sad-tear fa-lg', '#ff0000'),     
    }
    emoji, color = emoji_color.get(conditions, ('fa-circle-question', '#000'))
    return f'<i class="fa-solid {emoji}" style="color: {color}; margin-right: 6px;"></i>'