# -*- coding: utf-8 -*-

from diogenis.ldap_groups.models import LDAPGroup
from diogenis.accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User, Group
from diogenis.labs.models import Lesson
import ldap
import ldap.filter

class BaseGroupMembershipBackend(object):
	"""
	Base class for implementing an authentication backend which authenticates
	against LDAP and sets Django group membership based on LDAP Organizational
	Unit (OU) membership.
	"""
	def authenticate(self, username=None, password=None):
		"""
		Attempts to bind the provided username and password to LDAP.
		
		A successful LDAP bind authenticates the user.
		"""
		raise NotImplementedError
	
	def bind_ldap(self, username, password):
		"""
		Implements the specific logic necessary to bind a given username and
		password to the particular LDAP server.
		
		Override this method for each new variety of LDAP backend.
		"""
		raise NotImplementedError
	
	def get_or_create_user(self, username, password):
		"""
		Attempts to get the user from the Django db; failing this, creates a
		django.contrib.auth.models.User from details pulled from the specific
		LDAP backend.
		
		Override this method for each new variety of LDAP backend.
		"""
		raise NotImplementedError
	
	def get_user(self, user_id):
		"""
		Implements the logic to retrieve a specific user from the Django db.
		"""
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
		
	def set_memberships_from_ldap(self, user, membership):
		"""
		Assigns user to specific django.contrib.auth.models.Group groups based
		on ldap_group mappings created by the site admin, also assigns staff
		or superuser privileges based on those same mappings.
		"""
		ldap_groups = LDAPGroup.objects.filter(org_unit__in=membership)
		for l_grp in ldap_groups:
			for grp in l_grp.groups.all():
				user.groups.add(grp)
				
		staff_groups = ldap_groups.filter(make_staff=True).count()
		if staff_groups > 0:
			user.is_staff = True
			
		superuser_groups = ldap_groups.filter(make_superuser=True).count()
		if superuser_groups > 0:
			user.is_superuser = True
		user.save()
		

class ActiveDirectoryGroupMembershipSSLBackend(BaseGroupMembershipBackend):
	def bind_ldap(self, username, password):
		try:
			ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,settings.CERT_FILE)
		except AttributeError:
			pass
		ldap.set_option(ldap.OPT_REFERRALS,0)
		l = ldap.initialize(settings.LDAP_URL)
		l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
		binddn = "uid=%s,%s" % (username, settings.SEARCH_DN)
		l.simple_bind_s(binddn,password)
		return l
		
	def authenticate(self,username=None,password=None):
		try:
			if len(password) == 0:
				return None
			l = self.bind_ldap(username, password)
			l.unbind_s()
			return self.get_or_create_user(username,password)

		except ImportError:
			pass
		except ldap.INVALID_CREDENTIALS as e:
			pass
	
	def get_or_create_user(self, username, password):
		try:
			user = User.objects.get(username=username)
			
		except User.DoesNotExist:

			try:
				l = self.bind_ldap(username, password)

				# search
				result = l.search_s(settings.SEARCH_DN, ldap.SCOPE_SUBTREE, "(uid=%s)" % (username), ['*'])[0][1]

				first_name = result['cn'][0]

				last_name = result['sn'][0]

				username = result['username'][0]

				introduction_year = result['introductionYear'][0]

				registration_number = result['registrationNumber'][0]

				semester = result['semester'][0]
				mail = '%s@emptymail.com' % (username)

				'''if result.has_key('labs'):
					labs = ','.join(result['labs'])
				else:
					labs = None'''

				l.unbind_s()

				user = User(
					username = username,
					first_name = first_name,
					last_name = last_name,
					email = mail,
				)
			except Exception, e:
				return None
			user.is_staff = False
			user.is_superuser = False
			user.set_password(password)
			user.save()
			
			userprofile = UserProfile(
				user = user,
				is_teacher = False,
			)
			userprofile.save()
			
			authStudentProfile = AuthStudent(
				UserProfile = userprofile,
				am = registration_number,
				introduction_year = introduction_year,
				semester = semester,
			)
			authStudentProfile.save()

			if result.has_key('labs'):
				for lab in result['labs']:
					studentLessons = StudentToLesson(
						student = authStudentProfile,
						lesson = Lessons.objects.get(name = lab),
					)
					studentLessons.save()
		return user

class eDirectoryGroupMembershipSSLBackend(BaseGroupMembershipBackend):
	def bind_ldap(self, username, password):
		try:
			ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,settings.CERT_FILE)
		except AttributeError:
			pass
		l = ldap.initialize(settings.LDAP_URL)
		l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
		l.simple_bind_s(username, password)
		return l

	def authenticate(self,username=None,password=None):
		try:
			if len(password) == 0:
				return None
			l = self.bind_ldap(settings.BIND_USER, settings.BIND_PASSWORD)
			base = settings.SEARCH_DN
			scope = ldap.SCOPE_SUBTREE
			retrieve_attributes = ['cn']

			filtered_name = ldap.filter.escape_filter_chars(username)
			filter = 'cn=%s' % filtered_name

			results = l.search_s(base, scope, filter, retrieve_attributes)
			candidate_dns = [result[0] for result in results]

			l.unbind()
			for dn in candidate_dns:
				try:
					l = ldap.initialize(settings.LDAP_URL)
					l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
					l.simple_bind_s(dn, password)
				except ldap.INVALID_CREDENTIALS:
					l.unbind()
					continue
				l.unbind()
				return self.get_or_create_user(dn, password)

		except ImportError:
			pass
		except ldap.INVALID_CREDENTIALS:
			pass

	def get_or_create_user(self, username, password):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			try:
				l = self.bind_ldap(settings.BIND_USER, settings.BIND_PASSWORD)
				# search
				result = l.search_ext_s(settings.SEARCH_DN, ldap.SCOPE_SUBTREE, "uid=%s" % stripped_name,				settings.SEARCH_FIELDS)[0][1]
				l.unbind_s()

				last_name = result['sn'][0]
				first_name = result['cn'][0]
				user = User(username=stripped_name,first_name=first_name,last_name=last_name)
			except Exception, e:
				return None

			user.is_staff = False
			user.is_superuser = False
			user.set_password('ldap authenticated')
			user.save()

			self.set_memberships_from_ldap(user, membership)

		return user

