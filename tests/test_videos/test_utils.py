# -*- coding: utf-8 -*-
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

from django.test import TestCase
import pytest

from . import factories
from richard.videos.utils import generate_unique_slug


class TestGenerateUniqueSlug(TestCase):
    def test_slug_creation(self):
        """Slug is based on title."""
        v = factories.VideoFactory.build(title=u'Foo Bar')
        assert (
            generate_unique_slug(v, u'title', u'slug') ==
            u'foo-bar'
        )

    def test_unique_slug(self):
        """Generate unique slug using incrementing ending."""
        # These all have the same title, so subsequent videos get
        # a trailing count on the slug

        # This title is short! We want to check this so we don't chomp everything
        factories.VideoFactory.create_batch(title=u'Foo', size=5)

        v2 = factories.VideoFactory.build(title=u'Foo')
        assert (
            generate_unique_slug(v2, u'title', u'slug') ==
            u'foo-4'
        )

    def test_max_length_slug(self):
        # this is 51 characters long! We want to make sure we don't barf on lengthy titles
        title = u'Creating delicious APIs for Django apps since 2010.'
        factories.VideoFactory.create_batch(title=title, size=99)

        v2 = factories.VideoFactory.create(title=title)
        assert (
            v2.slug == u'creating-delicious-apis-for-django-apps-since-2-98'
        )
        # now that we've created 100 duplicates, we've run out of slugs.
        with pytest.raises(ValueError):
            factories.VideoFactory.create(title=title)

    def test_unicode_title(self):
        v = factories.VideoFactory.build(title=u'Nebenläufige Programme mit Python')
        assert (
            generate_unique_slug(v, u'title', u'slug') ==
            u'nebenlaufige-programme-mit-python'
        )
