/**
 * AFNANE PORTFOLIO 2026 — INTERACTION & ANIMATION LOGIC
 * High performance, zero external libraries, pure modern ES6+
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeaderScroll();
  initAnimatedStats();
  initCaseStudyNav();
  initPhoneMockupVideos();
  initLaptopScroll();
  initVideoModal();
  initBeforeAfterSlider();
  initScrollReveals();
  initMobileMenu();
  initBackToTop();
  initSmoothScroll();
  initApproachRadial();
  initScrollSpy();
  initTestimonialsSlider();
  initRecommendationModal();
});

/* --------------------------------------------------------------------------
   1. Header Scroll Effect
   -------------------------------------------------------------------------- */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const handleScroll = () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/* --------------------------------------------------------------------------
   2. Animated Statistics Counters
   -------------------------------------------------------------------------- */
function initAnimatedStats() {
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');
  if (!statNumbers.length) return;

  const statsObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target'), 10);
          if (isNaN(target)) return;
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          animateValue(el, 0, target, 1600, prefix, suffix);
          observer.unobserve(el);
        }
      });
    },
    { threshold: 0.3 }
  );

  statNumbers.forEach((num) => statsObserver.observe(num));

  function animateValue(obj, start, end, duration, prefix, suffix) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Ease out cubic
      const easeProgress = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(easeProgress * (end - start) + start);
      obj.textContent = `${prefix}${current}${suffix}`;
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        obj.textContent = `${prefix}${end}${suffix}`;
      }
    };
    window.requestAnimationFrame(step);
  }
}

/* --------------------------------------------------------------------------
   3. Case Studies Navigation (Floating Pill Navigation + Mobile Bar)
   -------------------------------------------------------------------------- */
function initCaseStudyNav() {
  const desktopNav = document.getElementById('caseEditorialIndex');
  const desktopLinks = document.querySelectorAll('.floating-pill-nav .pill-nav-item');
  const mobilePills = document.querySelectorAll('.case-nav-mobile-bar .case-mobile-pill');
  const articles = document.querySelectorAll('.case-study-article');
  const brandsSection = document.getElementById('brands');

  if (!articles.length) return;

  // Smooth scroll click handler
  const setupNavClicks = (links) => {
    links.forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('data-target') || link.getAttribute('href').replace('#', '');
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          const offsetTop = targetEl.getBoundingClientRect().top + window.pageYOffset - 90;
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  };

  setupNavClicks(desktopLinks);
  setupNavClicks(mobilePills);

  // Active state update function
  const setActiveCase = (targetId) => {
    desktopLinks.forEach((link) => {
      const id = link.getAttribute('data-target') || link.getAttribute('href').replace('#', '');
      link.classList.toggle('active', id === targetId);
    });

    mobilePills.forEach((pill) => {
      const id = pill.getAttribute('data-target') || pill.getAttribute('href').replace('#', '');
      const isActive = id === targetId;
      pill.classList.toggle('active', isActive);
      if (isActive && typeof pill.scrollIntoView === 'function') {
        pill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    });
  };

  // IntersectionObserver for tracking active case study
  const observerOptions = {
    root: null,
    rootMargin: '-15% 0px -40% 0px',
    threshold: [0, 0.1, 0.3, 0.5]
  };

  const visibleEntries = new Map();
  const caseObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      visibleEntries.set(entry.target.id, entry);
    });

    let bestId = null;
    let minTopDistance = Infinity;

    articles.forEach((art) => {
      const entry = visibleEntries.get(art.id);
      if (entry && entry.isIntersecting) {
        const topDist = Math.abs(entry.boundingClientRect.top - 120);
        if (topDist < minTopDistance) {
          minTopDistance = topDist;
          bestId = art.id;
        }
      }
    });

    if (bestId) {
      setActiveCase(bestId);
    }
  }, observerOptions);

  articles.forEach((art) => caseObserver.observe(art));

  // Visibility toggle for floating desktop index (strictly visible only while in Case Studies section)
  if (desktopNav && brandsSection) {
    const lastCase = articles[articles.length - 1] || brandsSection;

    const checkVisibility = () => {
      const brandsRect = brandsSection.getBoundingClientRect();
      const lastRect = lastCase.getBoundingClientRect();

      // Visible when Case Studies section is in reading view, and fades out as soon as case 06 exits
      const isWithinCases = brandsRect.top <= window.innerHeight * 0.45 && lastRect.bottom >= window.innerHeight * 0.25;
      desktopNav.classList.toggle('is-visible', isWithinCases);
    };

    window.addEventListener('scroll', checkVisibility, { passive: true });
    window.addEventListener('resize', checkVisibility, { passive: true });
    checkVisibility();
  }
}

/* --------------------------------------------------------------------------
   3b. iPhone Mockup Playable Video Reels Logic
   -------------------------------------------------------------------------- */
function initPhoneMockupVideos() {
  const phoneMockups = document.querySelectorAll('.iphone-mockup');
  if (!phoneMockups.length) return;

  const speakerMutedSvg = '<svg viewBox="0 0 24 24"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';
  const speakerUnmutedSvg = '<svg viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>';

  // 1. Playback observer: play when visible, pause when offscreen
  const videoPlaybackObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const mockup = entry.target;
        const video = mockup.querySelector('video');
        if (!video) return;

        if (entry.isIntersecting) {
          if (video.dataset.src && !video.src) {
            video.src = video.dataset.src;
          }
          if (!mockup.classList.contains('is-manually-paused')) {
            video.muted = true;
            video.defaultMuted = true;
            video.playsInline = true;
            const playPromise = video.play();
            if (playPromise !== undefined) {
              playPromise.catch(() => {});
            }
            mockup.classList.remove('is-paused');
          }
        } else {
          video.pause();
        }
      });
    },
    { threshold: 0.05, rootMargin: '200px 0px' }
  );

  phoneMockups.forEach((mockup) => {
    const video = mockup.querySelector('video');
    const audioBtn = mockup.querySelector('.video-audio-btn');
    const tapOverlay = mockup.querySelector('.video-tap-overlay');
    const statusIndicator = mockup.querySelector('.video-status-indicator');
    if (!video) return;

    // Enforce HTML5 autoplay policy compliance
    video.muted = true;
    video.defaultMuted = true;
    video.playsInline = true;
    video.setAttribute('muted', '');
    video.setAttribute('playsinline', '');
    video.setAttribute('autoplay', '');
    video.setAttribute('loop', '');

    videoPlaybackObserver.observe(mockup);

    const togglePlayPause = () => {
      if (video.dataset.src && !video.src) {
        video.src = video.dataset.src;
      }
      if (video.paused) {
        video.play().then(() => {
          mockup.classList.remove('is-paused');
          mockup.classList.remove('is-manually-paused');
          if (statusIndicator) {
            statusIndicator.classList.remove('is-active');
          }
        }).catch(() => {});
      } else {
        video.pause();
        mockup.classList.add('is-paused');
        mockup.classList.add('is-manually-paused');
        if (statusIndicator) {
          statusIndicator.classList.add('is-active');
        }
      }
    };

    if (tapOverlay) {
      tapOverlay.addEventListener('click', togglePlayPause);
    } else {
      video.addEventListener('click', togglePlayPause);
    }

    // Audio toggle button
    if (audioBtn) {
      audioBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isMuted = video.muted;
        
        if (isMuted) {
          // Mute all other videos first for clean single-audio listening
          document.querySelectorAll('.iphone-mockup video').forEach((otherVid) => {
            otherVid.muted = true;
            const parent = otherVid.closest('.iphone-mockup');
            if (parent) {
              const otherBtn = parent.querySelector('.video-audio-btn');
              if (otherBtn) otherBtn.innerHTML = speakerMutedSvg;
            }
          });

          video.muted = false;
          audioBtn.innerHTML = speakerUnmutedSvg;
        } else {
          video.muted = true;
          audioBtn.innerHTML = speakerMutedSvg;
        }
      });
    }
  });

  // 2. Influencer interactive reel and photo switchers (if any exist)
  document.querySelectorAll('.influencer-card').forEach((card) => {
    const video = card.querySelector('.mockup-reel-video');
    const photo = card.querySelector('.collab-photo-display');
    const switchBtns = card.querySelectorAll('[data-switch-video], [data-switch-photo]');

    switchBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        switchBtns.forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');

        if (btn.dataset.switchVideo && video) {
          const newSrc = btn.dataset.switchVideo;
          const newPoster = btn.dataset.switchPoster || '';
          video.src = newSrc;
          if (newPoster) video.poster = newPoster;
          video.load();
          video.muted = true;
          video.play().catch(() => {});
          const mockup = card.querySelector('.iphone-mockup');
          if (mockup) {
            mockup.classList.remove('is-paused', 'is-manually-paused');
          }
        } else if (btn.dataset.switchPhoto && photo) {
          photo.src = btn.dataset.switchPhoto;
        }
      });
    });
  });

  // 3. Proactively kickstart visible autoplay videos
  const kickstartVideos = () => {
    document.querySelectorAll('.mockup-reel-video').forEach((v) => {
      const parentMockup = v.closest('.iphone-mockup');
      if (parentMockup && parentMockup.classList.contains('is-manually-paused')) return;
      const rect = v.getBoundingClientRect();
      const inView = rect.top < window.innerHeight + 250 && rect.bottom > -250;
      if (inView && v.paused) {
        v.muted = true;
        v.defaultMuted = true;
        v.playsInline = true;
        const p = v.play();
        if (p !== undefined) p.catch(() => {});
      }
    });
  };

  window.addEventListener('scroll', kickstartVideos, { passive: true });
  window.addEventListener('resize', kickstartVideos, { passive: true });
  ['click', 'touchstart'].forEach((evt) => {
    window.addEventListener(evt, kickstartVideos, { once: true, passive: true });
  });
  setTimeout(kickstartVideos, 300);
}

/* --------------------------------------------------------------------------
   3c. Laptop Viewport Independent Scroll Logic
   -------------------------------------------------------------------------- */
function initLaptopScroll() {
  const laptopViewport = document.getElementById('tamazingLaptopViewport');
  if (!laptopViewport) return;

  // Prevent scroll trapping: when user hits top or bottom of laptop screen,
  // allow outer page scroll naturally
  laptopViewport.addEventListener('wheel', (e) => {
    const { scrollTop, scrollHeight, clientHeight } = laptopViewport;
    const isAtTop = scrollTop <= 2 && e.deltaY < 0;
    const isAtBottom = scrollTop + clientHeight >= scrollHeight - 2 && e.deltaY > 0;

    if (!isAtTop && !isAtBottom) {
      e.stopPropagation();
    }
  }, { passive: true });
}

/* --------------------------------------------------------------------------
   4. Universal Video Modal / Reel Player
   -------------------------------------------------------------------------- */
function initVideoModal() {
  const modal = document.getElementById('videoReelModal');
  const modalVideo = document.getElementById('modalVideoPlayer');
  const modalTitle = document.getElementById('modalVideoTitle');
  const modalSubtitle = document.getElementById('modalVideoSubtitle');
  const modalSource = document.getElementById('modalVideoSource');
  const closeBtn = document.getElementById('closeVideoModal');
  if (!modal || !modalVideo) return;

  // Open modal triggers
  const reelCards = document.querySelectorAll('[data-video-src]');
  reelCards.forEach((card) => {
    card.addEventListener('click', () => {
      const videoSrc = card.getAttribute('data-video-src');
      const title = card.getAttribute('data-video-title') || 'Featured Campaign Reel';
      const driveUrl = card.getAttribute('data-drive-url') || '#';

      // Detect brand context dynamically
      let brandName = card.getAttribute('data-brand');
      if (!brandName) {
        const parentCase = card.closest('.case-study-panel');
        if (parentCase) {
          const caseTitle = parentCase.querySelector('.case-title');
          if (caseTitle) brandName = caseTitle.textContent.trim();
        } else if (card.closest('#storytelling') || card.closest('#influencer')) {
          brandName = 'Visual Storytelling & UGC Campaign';
        }
      }

      modalVideo.src = videoSrc;
      if (modalTitle) modalTitle.textContent = title;
      if (modalSubtitle) {
        modalSubtitle.textContent = brandName ? `${brandName} • High Impact Reel` : 'Campaign Video • High Impact Reel';
      }

      if (modalSource) {
        if (driveUrl && driveUrl !== '#') {
          modalSource.style.display = 'inline-flex';
          modalSource.href = driveUrl;
          modalSource.textContent = 'View on Google Drive ↗';
        } else {
          modalSource.style.display = 'none';
        }
      }

      modal.classList.add('active');
      modalVideo.play().catch(() => {
        // Autoplay may be restricted without user interaction
      });
    });
  });

  // Close modal functions
  const closeModal = () => {
    modal.classList.remove('active');
    modalVideo.pause();
    modalVideo.currentTime = 0;
    modalVideo.src = '';
  };

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* --------------------------------------------------------------------------
   5. Interactive Before/After Slider (for Sani-Lux)
   -------------------------------------------------------------------------- */
function initBeforeAfterSlider() {
  const container = document.querySelector('.before-after-container');
  if (!container) return;

  const beforeWrap = container.querySelector('.before-img-wrap');
  const afterWrap = container.querySelector('.after-img-wrap');
  const handle = container.querySelector('.before-after-handle');
  if (!beforeWrap || !handle) return;

  // ARIA & accessibility attributes
  handle.setAttribute('tabindex', '0');
  handle.setAttribute('role', 'slider');
  handle.setAttribute('aria-valuenow', '50');
  handle.setAttribute('aria-valuemin', '0');
  handle.setAttribute('aria-valuemax', '100');
  handle.setAttribute('aria-label', 'Before and after comparison slider');

  let isDragging = false;

  const applyMask = (percentage) => {
    const clamped = Math.max(0, Math.min(100, percentage));
    const rounded = Math.round(clamped);

    // Apply clip-path to before wrap (reveals 0% -> clamped%)
    beforeWrap.style.webkitClipPath = `inset(0 ${100 - clamped}% 0 0)`;
    beforeWrap.style.clipPath = `inset(0 ${100 - clamped}% 0 0)`;

    // Apply clip-path to after wrap (reveals clamped% -> 100%)
    if (afterWrap) {
      afterWrap.style.webkitClipPath = `inset(0 0 0 ${clamped}%)`;
      afterWrap.style.clipPath = `inset(0 0 0 ${clamped}%)`;
    }

    handle.style.left = `${clamped}%`;
    handle.setAttribute('aria-valuenow', rounded);
  };

  const setSliderPosition = (x) => {
    const rect = container.getBoundingClientRect();
    let offsetX = x - rect.left;
    if (offsetX < 0) offsetX = 0;
    if (offsetX > rect.width) offsetX = rect.width;

    const percentage = rect.width > 0 ? (offsetX / rect.width) * 100 : 50;
    applyMask(percentage);
  };

  // Initialize at 50%
  applyMask(50);

  const onStart = (e) => {
    isDragging = true;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    setSliderPosition(clientX);
  };

  const onMove = (e) => {
    if (!isDragging) return;
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    setSliderPosition(clientX);
  };

  const onEnd = () => {
    isDragging = false;
  };

  container.addEventListener('mousedown', onStart);
  window.addEventListener('mousemove', onMove);
  window.addEventListener('mouseup', onEnd);

  container.addEventListener('touchstart', onStart, { passive: true });
  window.addEventListener('touchmove', onMove, { passive: true });
  window.addEventListener('touchend', onEnd);

  // Keyboard accessibility
  handle.addEventListener('keydown', (e) => {
    let current = parseFloat(handle.style.left) || 50;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
      e.preventDefault();
      applyMask(current - 5);
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
      e.preventDefault();
      applyMask(current + 5);
    } else if (e.key === 'Home') {
      e.preventDefault();
      applyMask(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      applyMask(100);
    }
  });
}

/* --------------------------------------------------------------------------
   6. Scroll Reveal Observer
   -------------------------------------------------------------------------- */
function initScrollReveals() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
  );

  reveals.forEach((el) => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight + 50) {
      el.classList.add('revealed');
    } else {
      revealObserver.observe(el);
    }
  });
}

/* --------------------------------------------------------------------------
   7. Mobile Menu
   -------------------------------------------------------------------------- */
function initMobileMenu() {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.nav-menu');
  const btnNavConnect = document.getElementById('btnNavConnect');
  if (!toggle || !nav) return;

  function toggleMenu(e) {
    if (e) e.preventDefault();
    const isOpen = nav.classList.toggle('mobile-open');
    toggle.classList.toggle('active');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  }

  toggle.addEventListener('click', toggleMenu);

  if (btnNavConnect) {
    btnNavConnect.addEventListener('click', (e) => {
      if (window.innerWidth <= 992) {
        toggleMenu(e);
      }
    });
  }

  const links = nav.querySelectorAll('a');
  links.forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('mobile-open');
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (
      nav.classList.contains('mobile-open') &&
      !nav.contains(e.target) &&
      !toggle.contains(e.target) &&
      (!btnNavConnect || !btnNavConnect.contains(e.target))
    ) {
      nav.classList.remove('mobile-open');
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Close menu on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('mobile-open')) {
      nav.classList.remove('mobile-open');
      toggle.classList.remove('active');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* --------------------------------------------------------------------------
   8. Back to Top Button
   -------------------------------------------------------------------------- */
function initBackToTop() {
  const backToTopBtn = document.querySelector('.back-to-top-btn');
  if (!backToTopBtn) return;

  backToTopBtn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  });
}

/* --------------------------------------------------------------------------
   9. Smooth Scroll for Anchor Links (with header offset)
   -------------------------------------------------------------------------- */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (!targetId || targetId === '#') return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        const headerOffset = 90;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth',
        });

        if (history.pushState) {
          history.pushState(null, '', targetId);
        }
      }
    });
  });
}

/* --------------------------------------------------------------------------
   10. Interactive 360° Radial Diagram Hover Linkage
   -------------------------------------------------------------------------- */
function initApproachRadial() {
  const container = document.getElementById('approach');
  if (!container) return;

  const elements = container.querySelectorAll('[data-approach]');
  if (!elements.length) return;

  function setHoverState(approachId, isHovered) {
    container.querySelectorAll(`[data-approach="${approachId}"]`).forEach((el) => {
      el.classList.toggle('is-hovered', isHovered);
    });
  }

  elements.forEach((el) => {
    const id = el.getAttribute('data-approach');
    if (!id) return;

    el.addEventListener('mouseenter', () => setHoverState(id, true));
    el.addEventListener('mouseleave', () => setHoverState(id, false));
    el.addEventListener('focus', () => setHoverState(id, true));
    el.addEventListener('blur', () => setHoverState(id, false));
  });
}

/* --------------------------------------------------------------------------
   11. Active Navigation Item Indicator (ScrollSpy)
   -------------------------------------------------------------------------- */
function initScrollSpy() {
  const mobileIndicator = document.getElementById('navSectionMobile');
  const desktopLinks = document.querySelectorAll('.nav-menu .nav-link');

  const sectionConfigs = [
    { id: 'hero', name: 'Home', navHref: '#hero' },
    { id: 'about', name: 'About', navHref: '#about' },
    { id: 'statsBar', name: 'About', navHref: '#about' },
    { id: 'journey', name: 'About', navHref: '#about' },
    { id: 'approach', name: 'Approach', navHref: '#approach' },
    { id: 'brands', name: 'Work', navHref: '#brands' },
    { id: 'influencer', name: 'Work', navHref: '#brands' },
    { id: 'testimonials', name: 'Testimonials', navHref: '#testimonials' },
    { id: 'recommendations', name: 'Testimonials', navHref: '#testimonials' },
    { id: 'contact', name: 'Contact', navHref: '#contact' }
  ];

  let currentActiveName = '';

  function setIndicatorText(newName) {
    if (!mobileIndicator) return;
    if (currentActiveName === newName) return;
    currentActiveName = newName;

    mobileIndicator.classList.add('changing');
    setTimeout(() => {
      mobileIndicator.textContent = newName;
      mobileIndicator.classList.remove('changing');
    }, 110);
  }

  function setActiveDesktopLink(targetHref) {
    desktopLinks.forEach(link => {
      if (link.getAttribute('href') === targetHref) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  function updateActive() {
    const scrollY = window.scrollY;
    const windowH = window.innerHeight;
    const docH = document.documentElement.scrollHeight;

    // 1. At very top of page -> Home
    if (scrollY < 120) {
      setIndicatorText('Home');
      setActiveDesktopLink('#hero');
      return;
    }

    // 2. Near bottom of page -> Contact
    if ((windowH + scrollY) >= (docH - 90)) {
      setIndicatorText('Contact');
      setActiveDesktopLink('#contact');
      return;
    }

    // 3. Focal point for section detection (35% down viewport)
    const focalY = scrollY + windowH * 0.35;

    let activeConfig = sectionConfigs[0];
    for (let i = 0; i < sectionConfigs.length; i++) {
      const el = document.getElementById(sectionConfigs[i].id);
      if (el) {
        const rect = el.getBoundingClientRect();
        const elTop = rect.top + scrollY;
        if (focalY >= elTop) {
          activeConfig = sectionConfigs[i];
        }
      }
    }

    setIndicatorText(activeConfig.name);
    setActiveDesktopLink(activeConfig.navHref);
  }

  let isTicking = false;
  window.addEventListener('scroll', () => {
    if (!isTicking) {
      window.requestAnimationFrame(() => {
        updateActive();
        isTicking = false;
      });
      isTicking = true;
    }
  }, { passive: true });

  window.addEventListener('resize', updateActive, { passive: true });
  updateActive();
}

/* --------------------------------------------------------------------------
   12. Testimonials Interactive Slider
   -------------------------------------------------------------------------- */
function initTestimonialsSlider() {
  const quoteEl = document.getElementById('testiQuoteText');
  const authorNameEl = document.getElementById('testiAuthorName');
  const authorRoleEl = document.getElementById('testiAuthorRole');
  const authorInfoEl = document.querySelector('.testi-author-info');
  const prevBtn = document.getElementById('testiPrevBtn');
  const nextBtn = document.getElementById('testiNextBtn');
  const dots = document.querySelectorAll('.testi-dot');
  if (!quoteEl || !authorNameEl || !authorRoleEl || !prevBtn || !nextBtn) return;

  const testimonials = [
    {
      quote: "“Afnane brings creativity, strategy and a deep understanding of digital marketing. She's a true asset who consistently translates brand identity into measurable growth.”",
      name: "M. Moussa",
      role: "Commercial Director — Moussa Real Estate"
    },
    {
      quote: "“Her strategic rigor, visual direction, and content execution delivered exceptional engagement across our luxury hospitality campaigns and direct booking channels.”",
      name: "Executive Direction",
      role: "Suites By Le Rêve Luxury Residences"
    },
    {
      quote: "“Rigorous, creative, and results-driven. Afnane elevated our digital identity, editorial campaigns, and creator collaborations to a premier international standard.”",
      name: "Brand Management",
      role: "TAMAZING Paris & Morocco"
    }
  ];

  let currentIndex = 0;
  let isAnimating = false;

  function setTestimonial(index) {
    if (isAnimating) return;
    isAnimating = true;

    // Fade out
    quoteEl.classList.add('fade-out');
    if (authorInfoEl) authorInfoEl.classList.add('fade-out');

    setTimeout(() => {
      currentIndex = (index + testimonials.length) % testimonials.length;
      const data = testimonials[currentIndex];

      quoteEl.textContent = data.quote;
      authorNameEl.textContent = data.name;
      authorRoleEl.textContent = data.role;

      dots.forEach((dot, idx) => {
        dot.classList.toggle('active', idx === currentIndex);
      });

      // Fade in
      quoteEl.classList.remove('fade-out');
      if (authorInfoEl) authorInfoEl.classList.remove('fade-out');

      setTimeout(() => {
        isAnimating = false;
      }, 320);
    }, 280);
  }

  prevBtn.addEventListener('click', () => setTestimonial(currentIndex - 1));
  nextBtn.addEventListener('click', () => setTestimonial(currentIndex + 1));

  dots.forEach((dot) => {
    dot.addEventListener('click', () => {
      const idx = parseInt(dot.getAttribute('data-index'), 10);
      if (!isNaN(idx) && idx !== currentIndex) {
        setTestimonial(idx);
      }
    });
  });
}

/* --------------------------------------------------------------------------
   14. Recommendation Letter Lightbox Modal
   -------------------------------------------------------------------------- */
function initRecommendationModal() {
  const modal = document.getElementById('letterModal');
  const closeBtn = document.getElementById('closeLetterModal');
  const modalImg = document.getElementById('modalLetterImg');
  const modalTitle = document.getElementById('modalLetterTitle');
  const modalPdfLink = document.getElementById('modalLetterPdfLink');
  const zoomBtn = document.getElementById('letterZoomBtn');
  const zoomText = document.getElementById('letterZoomBtnText');
  const letterTriggers = document.querySelectorAll('.rec-paper-wrapper, [data-open-letter]');

  if (!modal || !letterTriggers.length) return;

  const modalBody = modal.querySelector('.letter-modal-body');

  const setZoom = (isZoomed) => {
    if (!modalBody) return;
    if (isZoomed) {
      modalBody.classList.add('is-zoomed');
      if (zoomText) zoomText.textContent = 'Fit Page';
      if (modalImg) modalImg.title = 'Click to fit page in view';
    } else {
      modalBody.classList.remove('is-zoomed');
      if (zoomText) zoomText.textContent = 'Zoom In';
      if (modalImg) modalImg.title = 'Click to zoom into reading size';
    }
  };

  const openModal = (imgSrc, title, pdfUrl) => {
    if (modalImg) modalImg.src = imgSrc;
    if (modalTitle) modalTitle.textContent = title;
    if (modalPdfLink) {
      if (pdfUrl && pdfUrl !== '#') {
        modalPdfLink.href = pdfUrl;
        modalPdfLink.style.display = 'inline-flex';
      } else {
        modalPdfLink.style.display = 'none';
      }
    }
    setZoom(false);
    if (modalBody) modalBody.scrollTop = 0;

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    setZoom(false);
  };

  if (zoomBtn) {
    zoomBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (modalBody) {
        setZoom(!modalBody.classList.contains('is-zoomed'));
      }
    });
  }

  if (modalImg) {
    modalImg.addEventListener('click', (e) => {
      e.stopPropagation();
      if (modalBody) {
        setZoom(!modalBody.classList.contains('is-zoomed'));
      }
    });
  }

  letterTriggers.forEach((trigger) => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const card = trigger.closest('.rec-letter-card') || trigger;
      const wrapper = card.querySelector('.rec-paper-wrapper') || trigger;
      const imgSrc = wrapper.getAttribute('data-img');
      const title = wrapper.getAttribute('data-letter-title') || 'Recommendation Letter';
      const pdfUrl = wrapper.getAttribute('data-pdf') || '#';
      if (imgSrc) {
        openModal(imgSrc, title, pdfUrl);
      }
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
    }
  });
}



