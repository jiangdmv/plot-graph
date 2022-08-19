from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages

from census.models import Document
from census.forms import DocumentForm
from census.handledata import computeCount, plotCount, conclude

import pandas as pd
import numpy as np


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


def upload(request):
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()

            df = pd.read_csv(data.document, delimiter=data.filetype)
            target = data.target
            alpha = data.alpha

            if alpha >= 1 or alpha <= 0:
                messages.error(request, "Enter a valid alpha between 0 and 1")
                return redirect('upload')

            try:
                nums = df[target]
            except KeyError:
                messages.error(request, "Target " + target + " does not exist in the input file")
                return redirect('upload')

            # remove nan from the target column
            nums = nums[nums.notnull()]

            if len(nums) == 0:
                messages.error(request, "Target column cannot be empty")
                return redirect('upload')

            firstDigits = []
            for num in nums:
                try:
                    firstDigits.append(int(str(num)[0]))
                except ValueError:
                    messages.error(request, "The first digit in " + num + " is not a number")
                    return redirect('upload')

            firstDigits = np.array(firstDigits)
            firstDigits = firstDigits[firstDigits > 0]
            if len(firstDigits) == 0:
                messages.error(request, "First digits cannot be all 0")
                return redirect('upload')

            # Compute observed and expected counts
            [observed, expected] = computeCount(firstDigits)
            # Plot graph
            graphic = plotCount(observed, expected)
            # Perform Chi-square test for difference in distribution
            conclusion = conclude(observed, expected, alpha)

            return render(request, 'upload.html', {'form': form, 'graphic': graphic, "conclusion": conclusion})
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })


def delete_upload(request, id):
    if request.method == 'POST':
        uploadData = Document.objects.get(id=id)
        uploadData.delete()
    return redirect('/')
