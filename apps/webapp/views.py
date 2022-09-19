from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import FilmForm, PlanetForm, VehicleForm, SentientBeingForm, LanguageForm
from . models import Film, FilmCharacter, FilmPlanet, SentientBeing, Planet, Vehicle, Language


class AboutPageView(generic.TemplateView):
	template_name = 'webapp/about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['Films'] = Film.objects.all().count()
		context['SentientBeings'] = SentientBeing.objects.all().count()
		context['Planets'] = Planet.objects.all().count()
		context['Vehicles'] = Vehicle.objects.all().count()

		return context


class ContributerPageView(generic.TemplateView):
	template_name = 'webapp/contributers.html'


class DocsPageView(generic.TemplateView):
	template_name = 'webapp/docs.html'


@method_decorator(login_required, name='dispatch')
class FilmCreateView(generic.View):
	model = Film
	form_class = FilmForm
	success_message = "Film created successfully"
	template_name = 'webapp/film_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = FilmForm(request.POST)
		if form.is_valid():
			film = form.save(commit=False)
			film.save()

			for character in form.cleaned_data['characters']:
				FilmCharacter.objects.create(film=film, character=character)
			for planet in form.cleaned_data['planets']:
				FilmPlanet.objects.create(film=film, planet=planet)

			return redirect(film) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(film.get_absolute_url())

		return render(request, 'webapp/film_new.html', {'form': form})

	def get(self, request):
		form = FilmForm()
		return render(request, 'webapp/film_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class FilmDeleteView(generic.DeleteView):
	model = Film
	success_message = "Film deleted successfully"
	success_url = reverse_lazy('films')
	context_object_name = 'film'
	template_name = 'webapp/film_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete FilmJurisdiction entries
		FilmCharacter.objects \
			.filter(film_id=self.object.film_id) \
			.delete()
		FilmPlanet.objects \
			.filter(film_id=self.object.film_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class FilmDetailView(generic.DetailView):
	model = Film
	context_object_name = 'film'
	template_name = 'webapp/film_detail.html'

	def get_object(self):
		return super().get_object()


class FilmListView(generic.ListView):
	model = Film
	context_object_name = 'films'
	template_name = 'webapp/films.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Film.objects.all()
		# return SentientBeing.objects.select_related('homeworld').order_by('name')


class FilmPageView(generic.TemplateView):
	template_name = 'webapp/film_docs.html'


@method_decorator(login_required, name='dispatch')
class FilmUpdateView(generic.UpdateView):
	model = Film
	form_class = FilmForm
	context_object_name = 'film'
	success_message = "Film updated successfully"
	template_name = 'webapp/film_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		film = form.save(commit=False)
		film.save()

		# If any existing characters are not in updated list, delete them
		new_character_ids = []
		old_character_ids = FilmCharacter.objects \
			.values_list('character_id', flat=True) \
			.filter(film_id=film.film_id)

		# New Character list
		new_characters = form.cleaned_data['characters']

		# Insert new unmatched character entries
		for character in new_characters:
			new_id = character.sentient_being_id
			new_character_ids.append(new_id)
			if new_id in old_character_ids:
				continue
			else:
				FilmCharacter.objects \
					.create(film=film, character=character)

		# Delete old unmatched character entries
		for old_character_id in old_character_ids:
			if old_character_id in new_character_ids:
				continue
			else:
				FilmCharacter.objects \
					.filter(film_id=film.film_id, character_id=old_character_id) \
					.delete()

		# If any existing planets are not in updated list, delete them
		new_planet_ids = []
		old_planet_ids = FilmPlanet.objects \
			.values_list('planet_id', flat=True) \
			.filter(film_id=film.film_id)

		# New Planet list
		new_planets = form.cleaned_data['planets']

		# Insert new unmatched planet entries
		for planet in new_planets:
			new_id = planet.planet_id
			new_planet_ids.append(new_id)
			if new_id in old_planet_ids:
				continue
			else:
				FilmPlanet.objects \
					.create(film=film, planet=planet)

		# Delete old unmatched planet entries
		for old_planet_id in old_planet_ids:
			if old_planet_id in new_planet_ids:
				continue
			else:
				FilmPlanet.objects \
					.filter(film_id=film.film_id, planet_id=old_planet_id) \
					.delete()

		# return HttpResponseRedirect(film.get_absolute_url())
		return redirect('film_detail', pk=film.pk)


class HomePageView(generic.TemplateView):
	template_name = 'webapp/home.html'


@method_decorator(login_required, name='dispatch')
class PlanetCreateView(generic.View):
	model = Planet
	form_class = PlanetForm
	success_message = "Planet created successfully!"
	template_name = 'webapp/planet_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = PlanetForm(request.POST)
		if form.is_valid():
			planet = form.save(commit=False)
			planet.save()

		for planet in form.cleaned_data['planets']:
			Planet.objects.create(planet=planet)

		return render(request, 'webapp/planet_new.html', {'form': form})

	def get(self, request):
		form = PlanetForm()
		return render(request, 'webapp/planet_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PlanetDeleteView(generic.DeleteView):
	model = Planet
	success_message = "Planet deleted successfully!"
	success_url = reverse_lazy('planet')
	context_object_name = 'planet'
	template_name = 'webapp/planet_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete Planet entries
		Planet.objects \
			.filter(planet_id=self.object.planet_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class PlanetDetailView(generic.DetailView):
	model = Planet
	context_object_name = 'planets'
	template_name = 'webapp/planet_detail.html'

	def get_object(self):
		planet = super().get_object()
		return planet

class PlanetListView(generic.ListView):
	model = Planet
	context_object_name = 'planets'
	template_name = 'webapp/planets.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Planet.objects.all()
		# return SentientBeing.objects.select_related('homeworld').order_by('name')


class PlanetPageView(generic.TemplateView):
	template_name = 'webapp/planet_docs.html'


@method_decorator(login_required, name='dispatch')
class PlanetUpdateView(generic.UpdateView):
	model = Planet
	form_class = PlanetForm
	context_object_name = 'planet'
	success_message = "Planet updated successfully!"
	template_name = 'webapp/planet_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		planet = form.save(commit=False)
		planet.save()

		return HttpResponseRedirect(planet.get_absolute_url())


class RootPageView(generic.TemplateView):
	template_name = 'webapp/root.html'

#####work below#########################

@method_decorator(login_required, name='dispatch')
class SentientBeingCreateView(generic.View):
	model = SentientBeing
	form_class = SentientBeingForm
	success_message = "Sentient Being created successfully!"
	template_name = 'webapp/sentient_being_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = SentientBeingForm(request.POST)
		if form.is_valid():
			sentient_being = form.save(commit=False)
			sentient_being.save()

		for sentient_being in form.cleaned_data['sentient_being']:
			SentientBeing.objects.create(sentient_being=sentient_being)

		return render(request, 'webapp/sentient_being_new.html', {'form': form})

	def get(self, request):
		form = SentientBeingForm()
		return render(request, 'webapp/sentient_being_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class SentientBeingDeleteView(generic.DeleteView):
	model = SentientBeing
	success_message = "Sentient Being deleted successfully!"
	success_url = reverse_lazy('sentient_being')
	context_object_name = 'sentient_beings'
	template_name = 'webapp/sentient_being_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete Sentien tBeing entries
		SentientBeing.objects \
			.filter(sentient_being_id=self.object.sentient_being_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class SentientBeingDetailView(generic.DetailView):
	model = SentientBeing
	context_object_name = 'sentient_beings'
	template_name = 'webapp/sentient_being_detail.html'

	def get_object(self):
		sentient_being = super().get_object()
		return sentient_being


class SentientBeingListView(generic.ListView):
	model = SentientBeing
	context_object_name = 'sentient_beings'
	template_name = 'webapp/sentient_beings.html'
	# paginate_by = 20

	# def dispatch(self, *args, **kwargs):
	# 	return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return SentientBeing.objects.all()
		# return SentientBeing.objects.select_related('homeworld').order_by('name')


@method_decorator(login_required, name='dispatch')
class SentientBeingUpdateView(generic.UpdateView):
	model = SentientBeing
	form_class = SentientBeingForm
	context_object_name = 'sentient_being'
	success_message = "Sentient Being updated successfully!"
	template_name = 'webapp/sentient_being_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		sentient_being = form.save(commit=False)
		sentient_being.save()

		return HttpResponseRedirect(planet.get_absolute_url())



class SentientBeingPageView(generic.TemplateView):
	template_name = 'webapp/sentient_being_docs.html'


@method_decorator(login_required, name='dispatch')
class VehicleCreateView(generic.View):
	model = Vehicle
	form_class = VehicleForm
	success_message = "Vehicle created successfully"
	template_name = 'webapp/vehicle_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = VehicleForm(request.POST)
		if form.is_valid():
			vehicle = form.save(commit=False)
			vehicle.save()
			if form.cleaned_data['passengers']:
				for passenger in form.cleaned_data['passengers']:
					VehiclePassenger.objects.create(vehicle=vehicle, passenger=passenger)
			return HttpResponseRedirect(vehicle.get_absolute_url())

		return render(request, 'webapp/vehicle_new.html', {'form': form})

	def get(self, request):
		form = VehicleForm()
		return render(request, 'webapp/vehicle_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class VehicleDeleteView(generic.DeleteView):
	model = Vehicle
	success_message = "Vehicle deleted successfully"
	success_url = reverse_lazy('vehicles')
	context_object_name = 'vehicles'
	template_name = 'webapp/vehicle_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete VehiclePassenger entries
		VehiclePassenger.objects \
			.filter(vehicle_id=self.object.vehicle_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class VehicleDetailView(generic.DetailView):
	model = Vehicle
	context_object_name = 'vehicles'
	template_name = 'webapp/vehicle_detail.html'

	def get_object(self):
		return super().get_object()


class VehicleListView(generic.ListView):
	model = Vehicle
	context_object_name = 'vehicles'
	template_name = 'webapp/vehicles.html'

	def get_queryset(self):
		return Vehicle.objects.all()


class VehiclePageView(generic.TemplateView):
	template_name = 'webapp/vehicle_docs.html'


@method_decorator(login_required, name='dispatch')
class VehicleUpdateView(generic.UpdateView):
	model = Vehicle
	form_class = VehicleForm
	context_object_name = 'vehicles'
	success_message = "Vehicle updated successfully"
	template_name = 'webapp/vehicle_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		vehicle = form.save(commit=False)
		vehicle.save()

		return HttpResponseRedirect(vehicle.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class LanguageCreateView(generic.View):
	model = Language
	form_class = LanguageForm
	success_message = "Language created successfully"
	template_name = 'webapp/language_new.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = LanguageForm(request.POST)
		if form.is_valid():
			Language = form.save(commit=False)
			Language.save()
			if form.cleaned_data['passengers']:
				for language in form.cleaned_data['languages']:
					Language.objects.create(vehicle=vehicle, passenger=passenger)
			return HttpResponseRedirect(vehicle.get_absolute_url())

		return render(request, 'webapp/Language_new.html', {'form': form})

	def get(self, request):
		form = LanguageForm()
		return render(request, 'webapp/Language_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class LanguageDeleteView(generic.DeleteView):
	model = Language
	success_message = "Language deleted successfully"
	success_url = reverse_lazy('languages')
	context_object_name = 'languages'
	template_name = 'webapp/language_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete VehiclePassenger entries
		VehiclePassenger.objects \
			.filter(languages_id=self.object.languages_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


class LanguageDetailView(generic.DetailView):
	model = Language
	context_object_name = 'languages'
	template_name = 'webapp/language_detail.html'

	def get_object(self):
		return super().get_object()


class LanguageListView(generic.ListView):
	model = Vehicle
	context_object_name = 'languages'
	template_name = 'webapp/languages.html'

	def get_queryset(self):
		return Language.objects.all()


class LanguagePageView(generic.TemplateView):
	template_name = 'webapp/language_docs.html'


@method_decorator(login_required, name='dispatch')
class LanguageUpdateView(generic.UpdateView):
	model = Language
	form_class = LanguageForm
	context_object_name = 'languages'
	success_message = "Language updated successfully"
	template_name = 'webapp/language_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		language = form.save(commit=False)
		language.save()

		return HttpResponseRedirect(language.get_absolute_url())

