INSERT INTO "public".cemapp_typecredit
	(nom, description) VALUES ('Crédit aux particuliers','Vos besoins pour le quotidien sont à votre portée avec ce type de crédit que la Caisse d’Épargne de Madagascar vous offre.'),
                              ('Crédit aux Entrepreneurs','Ce crédit est destiné spécialement aux entrepreneurs et les petites et moyennes entreprises pour accroitre leurs activités, agrandir les infrastructures, renforcer les capitaux …');


INSERT INTO "public".cemapp_soustypecredit
	(nom, description, montant_min, montant_max, duree_min, duree_max, taux_interet, prefixe, type_credit_id) VALUES 
    ('Safidy', 'Le Crédit SAFIDY est spécialement conçu pour les besoins de consommation des fonctionnaires et travailleurs du secteur privé. Le montant que le salarié peut emprunter commence à partir de 300 000 Ar.', 300000, 19000000, 3, 24, '1.65', 'CSF', 1),
    ('Avotra Ainga', 'Le crédit AVOTRA est une aide d’appoint pour les entrepreneurs et les travailleurs indépendants afin qu’ils puissent accroître leurs activités. Le montant qui peut être emprunté commence à partir de 300 000 Ar.', 300000, 5000000, 3, 24, '2.20', 'CAAI', 2);


INSERT INTO "public".cemapp_client
	(nom, prenom, date_naissance, adresse, email, n_cin, statut_familial, nbr_dependant, situation_professionnelle, titre_emploie, nom_employeur, adresse_professionnelle, duree_emploie
, revenu_mensuel, depense_mensuelles, dettes_existantes, situation_bancaire, historique_credit, solde_bancaire, secteur_activite, type_contrat, valeur_actifs, historique_paiement)
VALUES
('Rabenanahary', 'Anjara', '1985-03-15', 'Antananarivo', 'rabenanahary.anjara@gmail.com', '123456789012', 'Marié(e)', 2,
 'Employé', 'Ingénieur', 'Tech Solutions', 'Antananarivo', 5, 2250000, 1000000, 250000, 'Bon',
 'Historique sans retard', 7500000.00, 'Informatique', 'CDI', 100000000.00, 'Paiements effectués à temps'), 
('Razananjakoto', 'Florence', '1990-06-20', 'Antananarivo', 'razananjakoto.florence@gmail.com', '987654321098', 'Célibataire', 0,
 'Indépendant', NULL, NULL, NULL, 0, 1750000.00, 750000.00, 0, 'Excellent',
 'Historique parfait', 5000000.00, 'Commerce', 'Freelance', 50000000.00, 'historique de paiement inexistant'),
('Rakotoarilala', 'Sedra', '1970-11-10', 'Antananarivo', 'rakotoarilala.sedra@gmail.com', '456789123045', 'Divorcé(e)', 1,
 'Sans emploi', NULL, NULL, NULL, 0, 500000.00, 400000.00, 100000.00, 'Faible',
 'Retards fréquents', 250000.00, 'aucun', 'Aucun', 2500000.00, 'Retards sur plusieurs échéances'),
('Rabetokotany', 'Miandry', '1980-01-25', 'Antananarivo', 'rabetokotany.miandry@gamil.com', '321654987012', 'Veuf/Veuve', 3,
 'Retraité', NULL, NULL, NULL, 0, 1000000.00, 600000.00, 0, 'Moyen',
 'Historique acceptable', 1500000.00, 'Agriculture', 'Aucun', 4000000.00, 'Paiements majoritairement à temps');