;; -*- no-byte-compile: t; -*-
;;; config/default/packages.el

(package! avy)
(package! ace-link)
(package! evil-nerd-commenter)

(unless (featurep! :editor evil)
  (package! expand-region))
