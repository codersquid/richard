# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.utils.six import text_type
from django.utils.text import slugify


def generate_unique_slug(obj, slug_from, slug_field='slug'):
    """ generate slug with trailing counts to prevent name collision """

    max_length = obj._meta.get_field(slug_field).max_length

    text = getattr(obj, slug_from)[:max_length]
    base_slug = slugify(text_type(text))
    slug = base_slug

    for i in range(100):
        if not obj.__class__.objects.filter(**{slug_field: slug}).exists():
            return slug
        suffix = text_type(i)
        slug = u'{}-{}'.format(base_slug[:max_length - len(suffix) - 1], suffix)

    raise ValueError('No valid slugs available.')
