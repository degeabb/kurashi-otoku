// Floating mini campaign banner — appears on scroll (desktop), dismissable.
(function () {
  var fb = document.getElementById('float-banner');
  if (!fb) return;

  var dismissed = false;
  try { dismissed = sessionStorage.getItem('fbDismissed') === '1'; } catch (e) {}

  var close = fb.querySelector('.fb-close');
  if (close) {
    close.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      dismissed = true;
      fb.classList.remove('show');
      try { sessionStorage.setItem('fbDismissed', '1'); } catch (e2) {}
    });
  }

  window.addEventListener('scroll', function () {
    if (dismissed) return;
    if (window.scrollY > 300) fb.classList.add('show');
    else fb.classList.remove('show');
  });
})();
