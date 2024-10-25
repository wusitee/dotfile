;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!
(setq +latex-viewers '(okular)) ;; set the defualt latex viewer to okular
(setq scroll-conservatively 101) ;; make the scroll better
(setq shell-file-name (executable-find "bash")) ;; set excutable shell to bash instead of fish
(setq-default vterm-shell (executable-find "fish")) ;; let v-term to use fish
(setq doom-font (font-spec :family "CaskaydiaCove Nerd Font" :size 17 ))
(setq vterm-timer-delay 0.01)
;; org mode config
(after! org
  (setq org-fontify-quote-and-verse-blocks nil
        org-fontify-whole-heading-line nil
        org-hide-leading-stars nil))
;; bind fuzzy find to SPC f h
(use-package! affe
  :config
  (setq affe-find-command "fd -t file -H")
  (map! :map doom-leader-file-map
        :desc "Fuzzy Find" "F" #'affe-find
        :desc "Fuzzy Find Home" "h" (lambda () (interactive) (affe-find "~"))))
;; activate SQL source code blocks
(org-babel-do-load-languages
 'org-babel-load-languages
 '((sql . t)))

;; use zoxide to change directory
(map!
 :map doom-leader-file-map
 "z" #'cd)

;; prevent client from creating new workspace
(after! persp-mode
  (setq persp-emacsclient-init-frame-behaviour-override "main"))

;; language tool
(after! langtool
  (setq langtool-default-language "en-GB"))

;; set org-mode latex-preview size
(setq org-format-latex-options (plist-put org-format-latex-options :scale 0.7))
;; keep latex preview on in org-mode
(after! org
  (setq org-startup-with-latex-preview t))

(use-package! websocket
  :after org-roam)

(use-package! org-roam-ui
  :after org-roam ;; or :after org
  ;;         normally we'd recommend hooking orui after org-roam, but since org-roam does not have
  ;;         a hookable mode anymore, you're advised to pick something yourself
  ;;         if you don't care about startup time, use
  ;;  :hook (after-init . org-roam-ui-mode)
  :config
  (setq org-roam-ui-sync-theme t
        org-roam-ui-follow t
        org-roam-ui-update-on-save t
        org-roam-ui-open-on-start t))

;; use org-morden
(use-package! org
  :hook (org-mode . org-modern-mode)
  :hook (org-agenda-finalize . org-modern-agenda)
  )

;; enable fragtop
(use-package! org-fragtog
  :hook
  (org-mode . org-fragtog-mode))


;; let emacs use okular as pdf browser
(setq doc-view-continuous t
      doc-view-resolver 'doc-view-okular)

;; force page break after toc
(setq org-latex-toc-command "\\clearpage \\tableofcontents \\clearpage")

;; tried to fix YASnippet templates not working in Latex fragments in org files
;; (add-hook! org-mode (yas-activate-extra-mode 'latex-mode))


;; for transparency
(set-frame-parameter nil 'alpha-background 90)
(add-to-list 'default-frame-alist '(alpha-background . 90))

(setq yas-snippet-dirs '("~/.config/doom/snippets/"))
;; solve the key conflict in while using yasinppets and org-mode
(defun yas/org-very-safe-expand ()
  (let ((yas/fallback-behavior 'return-nil)) (yas/expand)))
(add-hook 'org-mode-hook
          (lambda ()
            (make-variable-buffer-local 'yas/trigger-key)
            (setq yas/trigger-key [tab])
            (add-to-list 'org-tab-first-hook 'yas/org-very-safe-expand)
            (define-key yas/keymap [tab] 'yas-next-field)))


;; Inlay Hints
(after! lsp-mode
  (setq lsp-inlay-hint-enable t))

(setq user-full-name "wusitee"
      user-mail-address "kekdkkwk@outlook.com")

;; use anki-editor
(use-package! anki-editor
  :after org)

;; Doom exposes five (optional) variables for controlling fonts in Doom:
;;
;; - `doom-font' -- the primary font to use
;; - `doom-variable-pitch-font' -- a non-monospace font (where applicable)
;; - `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;; - `doom-symbol-font' -- for symbols
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face
;;
;; See 'C-h v doom-font' for documentation and more examples of what they
;; accept. For example:
;;
;; (setq doom-font (font-spec :family "Fira Code" :size 15 :weight 'semi-light)
;;      doom-variable-pitch-font (font-spec :family "Fira Sans" :size 13))
;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them
;; up, `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to
;; refresh your font settings. If Emacs still can't find your font, it likely
;; wasn't installed correctly. Font issues are rarely Doom issues!

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-one)

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type t)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")



;; Whenever you reconfigure a package, make sure to wrap your config in an
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.
;;
;;   (after! PACKAGE
;;     (setq x y))
;;
;; The exceptions to this rule:
;;
;;   - Setting file/directory variables (like `org-directory')
;;   - Setting variables which explicitly tell you to set them before their
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation).
;;   - Setting doom variables (which start with 'doom-' or '+').
;;
;; Here are some additional functions/macros that will help you configure Doom.
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces,
;; etc).
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.
