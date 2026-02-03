/**
 * Denture Fix Now - Theme JavaScript
 * Senior-Friendly Interactive Features
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initFAQ();
    initMobileMenu();
    initSmoothScroll();
    initFormValidation();
    initImageUpload();
  }

  /**
   * FAQ Accordion functionality
   */
  function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-question');
    
    faqItems.forEach(function(question) {
      question.addEventListener('click', function() {
        const faqItem = this.parentElement;
        const isActive = faqItem.classList.contains('active');
        
        // Close all FAQ items
        document.querySelectorAll('.faq-item').forEach(function(item) {
          item.classList.remove('active');
        });
        
        // Open clicked item if it wasn't active
        if (!isActive) {
          faqItem.classList.add('active');
        }
      });
    });
  }

  /**
   * Mobile menu toggle
   */
  function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('active');
        this.classList.toggle('active');
      });

      // Close menu when clicking outside
      document.addEventListener('click', function(event) {
        if (!menuToggle.contains(event.target) && !mobileMenu.contains(event.target)) {
          mobileMenu.classList.remove('active');
          menuToggle.classList.remove('active');
        }
      });
    }
  }

  /**
   * Smooth scrolling for anchor links
   */
  function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(function(link) {
      link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#' || href === '') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  /**
   * Form validation for better user experience
   */
  function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(function(form) {
      form.addEventListener('submit', function(e) {
        let isValid = true;
        const inputs = form.querySelectorAll('[required]');
        
        inputs.forEach(function(input) {
          if (!input.value.trim()) {
            isValid = false;
            showError(input, 'This field is required');
          } else {
            clearError(input);
          }
          
          // Email validation
          if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
              isValid = false;
              showError(input, 'Please enter a valid email address');
            }
          }
          
          // Phone validation (basic UK format)
          if (input.type === 'tel' && input.value.trim()) {
            const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/;
            if (!phoneRegex.test(input.value)) {
              isValid = false;
              showError(input, 'Please enter a valid phone number');
            }
          }
        });
        
        if (!isValid) {
          e.preventDefault();
        }
      });
      
      // Clear errors on input
      const inputs = form.querySelectorAll('input, textarea, select');
      inputs.forEach(function(input) {
        input.addEventListener('input', function() {
          clearError(this);
        });
      });
    });
  }

  function showError(input, message) {
    clearError(input);
    
    input.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    errorDiv.style.color = '#dc2626';
    errorDiv.style.fontSize = '1rem';
    errorDiv.style.marginTop = '0.5rem';
    
    input.parentNode.appendChild(errorDiv);
  }

  function clearError(input) {
    input.classList.remove('error');
    const error = input.parentNode.querySelector('.form-error');
    if (error) {
      error.remove();
    }
  }

  /**
   * Image upload preview
   */
  function initImageUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    fileInputs.forEach(function(input) {
      input.addEventListener('change', function() {
        const files = this.files;
        if (files && files[0]) {
          const reader = new FileReader();
          
          reader.onload = function(e) {
            // Find or create preview container
            let preview = input.parentNode.querySelector('.image-preview');
            if (!preview) {
              preview = document.createElement('div');
              preview.className = 'image-preview';
              preview.style.marginTop = '1rem';
              input.parentNode.appendChild(preview);
            }
            
            // Create image element
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '300px';
            img.style.maxHeight = '300px';
            img.style.borderRadius = '8px';
            img.style.border = '2px solid var(--color-border)';
            
            // Clear preview and add new image
            preview.innerHTML = '';
            preview.appendChild(img);
            
            // Add remove button
            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.textContent = 'Remove Image';
            removeBtn.className = 'btn btn--secondary';
            removeBtn.style.marginTop = '1rem';
            removeBtn.style.padding = '0.75rem 1.5rem';
            removeBtn.style.fontSize = '1rem';
            
            removeBtn.addEventListener('click', function() {
              input.value = '';
              preview.remove();
            });
            
            preview.appendChild(removeBtn);
          };
          
          reader.readAsDataURL(files[0]);
        }
      });
    });
  }

  /**
   * Add testimonials carousel (if needed)
   */
  function initTestimonialCarousel() {
    const carousel = document.querySelector('.testimonials-carousel');
    if (!carousel) return;
    
    const items = carousel.querySelectorAll('.testimonial');
    let currentIndex = 0;
    
    function showTestimonial(index) {
      items.forEach(function(item, i) {
        item.style.display = i === index ? 'block' : 'none';
      });
    }
    
    // Show first testimonial
    showTestimonial(0);
    
    // Auto-rotate every 5 seconds
    setInterval(function() {
      currentIndex = (currentIndex + 1) % items.length;
      showTestimonial(currentIndex);
    }, 5000);
  }

  /**
   * Accessibility improvements
   */
  function improveAccessibility() {
    // Add ARIA labels to buttons without text
    const buttons = document.querySelectorAll('button:not([aria-label])');
    buttons.forEach(function(button) {
      if (!button.textContent.trim() && !button.getAttribute('aria-label')) {
        button.setAttribute('aria-label', 'Button');
      }
    });
    
    // Ensure all images have alt text
    const images = document.querySelectorAll('img:not([alt])');
    images.forEach(function(img) {
      img.setAttribute('alt', '');
    });
  }

  // Call accessibility improvements
  improveAccessibility();

})();
