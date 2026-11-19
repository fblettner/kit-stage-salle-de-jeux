import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { useMemo, useRef, useEffect } from 'react'

marked.setOptions({ gfm: true, breaks: false })

// Affiche du Markdown (le texte des fichiers .md du kit), avec un bouton « Copier » sur chaque bloc de code.
export default function Markdown({ texte, className = '' }) {
  const html = useMemo(() => DOMPurify.sanitize(marked.parse(texte || '')), [texte])
  const ref = useRef(null)

  useEffect(() => {
    const zone = ref.current
    if (!zone) return
    zone.querySelectorAll('pre').forEach((pre) => {
      if (pre.querySelector('.copier-mini')) return
      const bouton = document.createElement('button')
      bouton.className = 'copier-mini'
      bouton.textContent = 'Copier'
      bouton.onclick = () => {
        copier(pre.querySelector('code')?.innerText ?? pre.innerText)
        bouton.textContent = '✓ Copié'
        setTimeout(() => (bouton.textContent = 'Copier'), 1500)
      }
      pre.appendChild(bouton)
    })
    zone.querySelectorAll('a[href^="http"]').forEach((a) => {
      a.target = '_blank'
      a.rel = 'noreferrer'
    })
  }, [html])

  return <div ref={ref} className={`markdown ${className}`} dangerouslySetInnerHTML={{ __html: html }} />
}

export function copier(texte) {
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(texte).catch(() => copierALAncienne(texte))
  } else {
    copierALAncienne(texte)
  }
}

function copierALAncienne(texte) {
  const zone = document.createElement('textarea')
  zone.value = texte
  document.body.appendChild(zone)
  zone.select()
  try {
    document.execCommand('copy')
  } catch {
    // tant pis
  }
  zone.remove()
}
