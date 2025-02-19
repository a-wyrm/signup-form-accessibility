17436
82% are serious issues

TikTok as a case study
adtargeting.io as a case study for good forms

I only apply 3.3.2 Labels or Instructions iff there is BOTH non-required fields and required fields that are not labelled as such
I only apply JavaScript 05 iff there is no way for the user to see their password
I apply 3.3.4 Redundant Entry iff a user is required to re-enter a password and there is no way to view or copypaste a password from the original password field

Subtle issues with sign up forms:
Passwords don't allow the user to see their password. This can especially be an issue if the user is required to re-enter a password.
Sign up forms having both registry and sign in forms and are not labelled properly.
Errors are not properly highlighted using either an alert, aria-live, or aria-invalid labels.

Pop-ups with form elements in them are also evaluated. On Input is added if a pop up takes priority input and doesn't inform the user that it is a popup using aria labels or alerts