#  Copyright 2019 Simon Zigelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .forms import CongregationForm


@login_required
def choose_console(request):
    if request.method == 'POST':
        form = CongregationForm(request.POST)
        if form.is_valid():
            congregation = form.cleaned_data["congregation"].congregation
            return HttpResponseRedirect("/console/%s" % congregation)
    else:
        form = CongregationForm()
    return render(request, "console/choose_console.html", {"form": form})


@login_required
def console(request, congregation):
    return render(request, "console/console.html", {"congregation_ws": mark_safe(congregation)})
