%% Clear memory, screen, and close all figures

clear, clc, close all;

%% Definizione delle funzioni di stato

process = {
     @(k, xkm1, xkm2, xkm3, uk) xkm1/2 + 25*xkm2/(1+xkm2^2) + 8*cos(1.2*k) + uk;
     %@(k, xkm1, xkm2, xkm3, uk) xkm2 + 10*xkm1/(1+xkm3^2) + 4*sin(1.2*k) + uk;
     @(k, xkm1, xkm2, xkm3, uk) xkm3/2 + 6*xkm2/(1+1*xkm2^2) + 4*cos(1.2*k) + uk;
     %@(k, xkm1, xkm2, xkm3, uk) xkm1/2 + 25*xkm2/(1+xkm2^2) + 8*cos(1.2*k) + uk;
     %@(k, xkm1, xkm2, xkm3, uk) xkm1/2 + 25*xkm2/(1+xkm2^2) + 8*cos(1.2*k) + uk;
     %@(k, xkm1, xkm2, xkm3, uk) xkm2 + 25*xkm1/(1+xkm1^2) + 8*cos(1.2*k) + uk;
     @(k, xkm1, xkm2, xkm3, uk) xkm1/2 + 25*xkm3/(1+xkm3^2) + 8*cos(1.2*k) + uk;
};

%% Definizione delle funzione di osservazione

obs = {
      @(xk, vk) xk^2/20 + vk;
      @(xk, vk) xk^2/20 + vk;  
      @(xk, vk) xk^2/20 + vk;  
 };                               

%% Definizione variabili

dimension =size(process,1);                           % Numero degli stati
particelle = 200;                                     % Numero delle particelle
T = 50;                                               % Intervallo di tempo  
passo=T/particelle;                                   % Tempo di campionamento

nx = dimension;                                       % Dimensione del vettore degli stati

ny = dimension;                                       % Dimensione del vettore delle osservazioni

%% Rumore degli stati: Def.della PDF del rumore e della funzione generatrice del rumore 

nu = dimension;                                       % Dimensione del vettore di rumore di stato                                 
sigma_u = sqrt(10);                                   % Varianza
p_sys_noise   = @(u) normpdf(u, 0, sigma_u);          % PDF del rumore di stato
gen_sys_noise = @(u) normrnd(0, sigma_u);             % Funzione generatrice del rumore di stato 

%% Rumore delle osservazioni: Def.della PDF del rumore e della funzione generatrice del rumore 

nv = dimension;                                       % Dimensione del vettore di rumore delle osservazioni
sigma_v = sqrt(1);                                    % Varianza
p_obs_noise   = @(v) normpdf(v, 0, sigma_v);          % PDF del rumore delle osservazioni
gen_obs_noise = @(v) normrnd(0, sigma_v);             % Funzione generatrice del rumore delle osservazioni

%% Inizializzazione della PDF di stato

gen_x0 = @(x) normrnd(0, sqrt(10));

%% Likelihood PDF delle osservazioni p(y[k] | x[k])

p_yk_given_xk = @(yk, xk, n) p_obs_noise(yk - obs{n}(xk, 0));

%% Separazione dello spazio di memoria (Non filtrati)

x = zeros(nx,T);                                      % Vettore degli stati
y = zeros(ny,T);                                      % Vettore delle osservazioni
u = zeros(nu,T);                                      % Vettore del rumore di stato
v = zeros(nv,T);                                      % Vettore del rumore delle osservazioni

%% Simulazione del sistema

% Inizializzazione dello stato
xh0 = 0;                                     

% Inizializzazione dei processi di rumore, di stato,di osservazione
for n=1:nx
    u(n,1) = 0;                               
    v(n,1) = gen_obs_noise(sigma_v);          
    x(n,1) = xh0;
    y(n,1) = obs{n}(xh0, v(n,1));
end

% Simulazione dei processi di rumore, di stato e di osservazione
for k = 2:T 
    for n=1:nx
       u(n,k) = gen_sys_noise();             
       v(n,k) = gen_obs_noise();              
       x(n,k) = process{n}(k, x(1,k-1), x(2,k-1), x(3,k-1), u(1,k-1));
       y(n,k) = obs{n}(x(n,k), v(n,k));
    end
end

%% ????????????????????????????????????????

dev=0;
if(dev==1)
    figure;

    for i=1:nx
        ax = subplot(nx,1,i); 
        plot(ax,1:T,y(i,:),'b');
        title(['Osservazioni - N.Oss - ',num2str(i)])
    end
    
    figure;
    for i=1:nx
        ax = subplot(nx,1,i); 
        plot(ax,1:T,x(i,:),'b');
        title(['Stato non filtrato - N.Stati - ',num2str(i)])
    end
    
    return;
end

%% Separazione dell spazio di memoria (Filtrati)

xh = zeros(nx, T);                                 % Vettore degli stati 
yh = zeros(ny, T);                                 % Vettore delle osservazioni 

%% Inizializzazione dei processi di stato e osservazione filtrati
for n=1:nx
    xh(n,1) = xh0;
    yh(n,1) = obs{n}(xh0, 0);
end

%% Definizione degli elementi del particle filter

pf.k               = 1;                           % Inizializzazione delle iterazioni (istanti di tempo)
pf.Ns              = particelle;                  % Numero di particelle
pf.w               = zeros(pf.Ns, T);             % Pesi delle particelle
pf.particles       = zeros(1, pf.Ns, T);          % Vettore delle particelle
pf.gen_x0          = gen_x0;                      % Funzione generatrice campioni-Inizzializzazione delle PDF di stato
pf.p_yk_given_xk   = p_yk_given_xk;               % Funzione likelihood PDF p(y[k] | x[k])
pf.gen_sys_noise   = gen_sys_noise;               % Funzione generatrice del rumore di stato

%% Stima degli stati e delle osservazioni
for n=1:nx
    
   for k = 2:T
       
       fprintf('Iteration = %d/%d\n',k,T);
       pf.k = k;
       [xh(n,k), pf] = particle_filter(process{n}, y(n,k), pf, 'systematic_resampling');  % Stima degli stati
       yh(n,k) = obs{n}(xh(n,k), 0);                                                      % Stima delle osservazioni 
     
    end
end

%% Plottaggi dei risultati

% Plot delle osservazioni 
figure;

    for i=1:nx
        
        ax = subplot(nx,1,i); 
        plot(ax,1:T,y(i,:),'b', 1:T,yh(i,:),'r');
        title(['Osservazioni vs Osservazioni filtrate dal particle filter - N.Obs - ',num2str(i)])
    end

% Plot degli stati 
figure;
    for i=1:nx
        ax = subplot(nx,1,i); 
        plot(ax,1:T,x(i,:),'b', 1:T,xh(i,:),'r');
        title(['Stati vs Stati filtrati dal particle filter - N.State - ',num2str(i)])
    end
    
return;
