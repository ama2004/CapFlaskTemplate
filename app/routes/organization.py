#attempt



# These routes are an example of how to use data, forms and routes to create
# a forum where a posts and comments on those posts can be
# Created, Read, Updated or Deleted (CRUD)

from flask.helpers import url_for
from app import app, login
import mongoengine.errors
from flask import render_template, flash, redirect
from flask_login import current_user
from app.classes.data import Organization
from app.classes.forms import OrganizationForm
from flask_login import login_required
import datetime as dt

# This is the route to list all posts
@app.route('/organization/list')
# This means the user must be logged in to see this page
@login_required
def organizationList():
    # This retrieves all of the 'posts' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'posts'.
    organizations = Organization.objects()
    # This renders (shows to the user) the posts.html template. it also sends the posts object 
    # to the template as a variable named posts.  The template uses a for loop to display
    # each post.
    return render_template('organizations.html',organizations=organizations)

# This route renders a form for the user to create a new post
@app.route('/organization/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def organizationNew():
    # This gets a form object that can be displayed on the template
    form = OrganizationForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new post form. 
        # Post() is a method for creating a new post. 'newPost' is the variable where the object
        # that is the result of the Post() method is stored.  
        newOrganization = Organization(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            name = form.name.data,
            website = form.website.data,
            address = form.address.data,
            summary = form.summary.data,
            mentorship = form.mentorship.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modifydate = dt.datetime.utcnow
        )
        # This is a metod that saves the data to the mongoDB database.
        newOrganization.save()

        return redirect(url_for('organization',organizationID=newOrganization.id))

    return render_template('organizationform.html',form=form)

@app.route('/organization/<organizationID>')
@login_required
def organization(organizationID):
    organization = Organization.objects.get(id=organizationID)

    return render_template('organization.html', organization=organization)

@app.route('/organization/delete/<organizationID>')
@login_required
def organizationDelete(organizationID):
    deleteOrganization = Organization.objects.get(id=organizationID)
    if current_user == deleteOrganization.author:
        deleteOrganization.delete()
        flash('The organization was deleted.')
    else:
        flash("You can't delete an organization you don't own.")
    organizations = Organization.objects()  
    return render_template('organizations.html',organizations=organizations)



@app.route('/organization/edit/<organizationID>', methods=['GET', 'POST'])
@login_required
def organizationEdit(organizationID):
    editOrganization = Organization.objects.get(id=organizationID)
    if current_user != editOrganization.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('organization',organizationID=organizationID))
    form = OrganizationForm()
    if form.validate_on_submit():
        editOrganization.update(
            name = form.name.data,
            website = form.website.data,
            address = form.address.data,
            summary = form.summary.data,
            mentorship = form.mentorship.data,
            modifydate = dt.datetime.utcnow
        )
        return redirect(url_for('organization',organizationID=organizationID))

    form.name.data = editOrganization.name
    form.website.data = editOrganization.website
    form.address.data = editOrganization.address
    form.summary.data = editOrganization.summary
    form.mentorship.data = editOrganization.mentorship

    return render_template('organizationform.html',form=form)