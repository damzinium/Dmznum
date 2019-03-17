from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class AccountsStaticSitemap(Sitemap):
	def items(self):
		return ['login', 'register']

	def location(self, item):
		return reverse(f'accounts:{item}')
