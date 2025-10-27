from flask import render_template, redirect, url_for, flash, current_app
from . import resume_bp
from .forms import ContactForm


@resume_bp.route("/resume")
def resume() -> str:
    return render_template("resume.html", title="Resume")


@resume_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger_message = f"Received contact form submission from {form.email.data}. "\
                         f"Name: {form.name.data}, "\
                         f"Subject: {form.subject.data}, "\
                         f"Phone: {form.phone.data}, "\
                         f"Message: {form.message.data}"
        current_app.logger.info(logger_message)
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("resume.contact"))
    if form.errors != {}:
        flash("There were some errors in your form. Please correct them and try again.", "danger")
    return render_template("contact.html", title="Contact", contact_form=form)