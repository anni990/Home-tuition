from flask import url_for

def get_fallback_image(category):
    """
    Returns a fallback image URL from Unsplash based on the category.
    """
    fallback_images = {
        'hero': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&h=800',
        'mission': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&h=600',
        'team': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?auto=format&fit=crop&w=400&h=400',
        'tutor': 'https://images.unsplash.com/photo-1606330194905-4342812573e8?auto=format&fit=crop&w=400&h=400',
        'student': 'https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?auto=format&fit=crop&w=400&h=400',
        'subject': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=800&h=600',
        'default': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&h=600'
    }
    return fallback_images.get(category, fallback_images['default'])

def get_icon_fallback(category):
    """
    Returns a fallback icon class based on the category.
    """
    icon_map = {
        'user': 'fas fa-user',
        'tutor': 'fas fa-chalkboard-teacher',
        'subject': 'fas fa-book',
        'hero': 'fas fa-graduation-cap',
        'testimonial': 'fas fa-quote-right',
        'feature': 'fas fa-star',
        'social': {
            'facebook': 'fab fa-facebook',
            'twitter': 'fab fa-twitter',
            'instagram': 'fab fa-instagram',
            'linkedin': 'fab fa-linkedin'
        }
    }
    
    if isinstance(icon_map.get(category), dict):
        return icon_map.get(category, {}).get('default', 'fas fa-image')
    return icon_map.get(category, 'fas fa-image')

def get_image_url(image_path, category='default', social_platform=None):
    """
    Returns either the image URL if the image exists, or creates an icon element if it doesn't.
    """
    if not image_path or not image_path.strip():
        if category == 'social' and social_platform:
            icon_class = get_icon_fallback('social').get(social_platform, 'fas fa-share')
        else:
            icon_class = get_icon_fallback(category)
        return f'<i class="{icon_class}"></i>'
    
    try:
        return url_for('static', filename=image_path)
    except:
        if category == 'social' and social_platform:
            icon_class = get_icon_fallback('social').get(social_platform, 'fas fa-share')
        else:
            icon_class = get_icon_fallback(category)
        return f'<i class="{icon_class}"></i>' 