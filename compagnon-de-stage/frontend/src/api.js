import { useCallback, useEffect, useState } from 'react'

// Les appels au serveur. Le « jeton » (reçu à la connexion) est gardé dans le navigateur
// pour ne pas avoir à se reconnecter à chaque fois.

const CLE = 'compagnon-jeton'

export function lireJeton() {
  try {
    return localStorage.getItem(CLE) || ''
  } catch {
    return ''
  }
}

export function ecrireJeton(jeton) {
  try {
    if (jeton) localStorage.setItem(CLE, jeton)
    else localStorage.removeItem(CLE)
  } catch {
    // navigation privée : tant pis, il faudra se reconnecter
  }
}

let quandDeconnecte = () => {}
export function surDeconnexion(fn) {
  quandDeconnecte = fn
}

export async function api(chemin, { methode = 'GET', corps, texte = false } = {}) {
  const options = {
    method: methode,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${lireJeton()}`,
    },
  }
  if (corps !== undefined) options.body = JSON.stringify(corps)
  const reponse = await fetch(`/api${chemin}`, options)
  if (reponse.status === 401 && !chemin.startsWith('/connexion')) {
    ecrireJeton('')
    quandDeconnecte()
  }
  if (!reponse.ok) {
    let message = `Erreur ${reponse.status}`
    try {
      const d = await reponse.json()
      if (typeof d.detail === 'string') message = d.detail
      else if (Array.isArray(d.detail)) message = 'Vérifie ce que tu as écrit (champ vide ou trop long ?)'
    } catch {
      // pas de JSON
    }
    throw new Error(message)
  }
  return texte ? reponse.text() : reponse.json()
}

// L'entrée « La salle de jeux » du menu : les 4 jeux d'exemple, affichés dans le compagnon
export function lienSalle(programme) {
  if (!programme.salle) return null
  return { cle: 'salle', nom: 'La salle de jeux', icone: 'jouer', pleine: true, description: "Les 4 jeux d'exemple : joue, observe, inspire-toi" }
}

// Un petit utilitaire : la même chose qu'un useEffect + fetch, avec rechargement régulier

export function useApi(chemin, { toutesLes = 0 } = {}) {
  const [donnees, setDonnees] = useState(null)
  const [erreur, setErreur] = useState('')
  const recharger = useCallback(async () => {
    if (!chemin) return
    try {
      setDonnees(await api(chemin))
      setErreur('')
    } catch (e) {
      setErreur(e.message)
    }
  }, [chemin])
  useEffect(() => {
    recharger()
    if (!toutesLes) return
    const id = setInterval(() => {
      if (document.visibilityState === 'visible') recharger()
    }, toutesLes * 1000)
    return () => clearInterval(id)
  }, [recharger, toutesLes])
  return { donnees, erreur, recharger, setDonnees }
}
