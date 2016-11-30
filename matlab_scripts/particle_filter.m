function [xhk, pf] = particle_filter(sys, yk, pf, resampling_strategy)

k = pf.k;                                   %Tempo

% Verifica che l'istante di tempo k  parta da 2
if k == 1
   error('error: k must be an integer greater or equal than 2');
end

%% Inizializzazione delle variabili del particle filter

Ns = pf.Ns;                                 % Numero di particelle
nx = size(pf.particles,1);                  % Numero di stati
wkm1 = pf.w(:, k-1);                        % Peso dell'ultima iterazione


%% Inizializzazione filtraggio: 
% Prima iterazione, vengono generate particelle "casuali" alle quali vengono assegnati gli stessi pesi

if k == 2
% Simulazione delle particelle iniziali    
   for i = 1:Ns                            
        pf.particles(:,i,1) = pf.gen_x0();  
   end
% Tutte le particelle hanno lo stesso peso   
   wkm1 = repmat(1/Ns, Ns, 1);              
   
end

%% Separazione dello spazio di memoria

% Inizializzazione dei vettori degli stati agli istanti precedenti
xkm1 = pf.particles(1,:,k-1);               % Estrazione delle particelle dalla k-1 iterazione dello stato 1
xkm2 = pf.particles(1,:,k-1);               % Estrazione delle particelle dalla k-1 iterazione dello stato 2
xkm3 = pf.particles(1,:,k-1);               % Estrazione delle particelle dalla k-1 iterazione dello stato 3

% Inizializzazione vettori
xk   = zeros(size(xkm1));                   % Stato filtrato

wk   = zeros(size(wkm1));                   % Pesi

%% Algoritmo Particle Filter

for n=1:nx
    
    for i = 1:Ns
         
        xk(:,i) = sys(k, xkm1(1), xkm2(1), xkm3(1), pf.gen_sys_noise());  % calcolo dello stato filtrato

        wk(i) = wkm1(i) * pf.p_yk_given_xk(yk, xk(n,i), n);               % calcolo dei pesi
      
    end
end

%% Normalizzazione del vettore dei pesi

wk = wk./sum(wk);

%% Calcolo della dimensione effettiva dei campioni

Neff = 1/sum(wk.^2);

%% Resampling

resample_percentaje = 0.50;
Nt = resample_percentaje*Ns;
if Neff < Nt
    
   disp('Resampling ...')
   [xk, wk] = resample(xk, wk, resampling_strategy);
   
end

%% Calcolo dello stato stimato

xhk = zeros(nx,1);
for i = 1:Ns;
   xhk = xhk + wk(i)*xk(:,i);
end

%% Store dei nuovi pesi e delle nuove particelle

pf.w(:,k) = wk;
pf.particles(:,:,k) = xk;

return; 

%% Funzione di Resampling

function [xk, wk, idx] = resample(xk, wk, resampling_strategy)

Ns = length(wk);  

switch resampling_strategy
    
   case 'multinomial_resampling'
       
      with_replacement = true;
      idx = randsample(1:Ns, Ns, with_replacement, wk);
   
   case 'systematic_resampling'
     
      edges = min([0 cumsum(wk)'],1); 
      edges(end) = 1;                 
      u1 = rand/Ns;

      [~, idx] = histc(u1:1/Ns:1, edges);

   otherwise
       
      error('Resampling strategy not implemented')
end;


xk = xk(:,idx);                    % Estrazione delle nuove particelle
wk = repmat(1/Ns, 1, Ns);          % Pesi delle nuove particelle tutti uguali

return; 
