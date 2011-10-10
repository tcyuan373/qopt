% ======================================================== % 
% Files of the Matlab programs included in the book:       %
% Xin-She Yang, Nature-Inspired Metaheuristic Algorithms,  %
% Second Edition, Luniver Press, (2010).   www.luniver.com %
% ======================================================== %                               

% Simulated Annealing for constrained optimization
% by Xin-She Yang @ Cambridge University @2008
% Usage: sa_mincon(0.99) or sa_mincon;

function [bestsol,fval,N]=sa_mincon(alpha)
% Default cooling factor
if nargin<1,
    alpha=0.95;
end

% Display usage
help sa_mincon.m
disp('sa_mincon or [Best,fmin,N]=sa_mincon(0.9)');

% Welded beam design optimization
Lb=[0.1 0.1  0.1 0.1];
Ub=[2.0 10.0 10.0 2.0];
u0=Lb+(Ub-Lb).*rand(size(Lb));

if length(Lb) ~=length(Ub),
    disp('Simple bounds/limits are improper!');
    return
end

%% Start of the main program -------------------------
d=length(Lb);       % Dimension of the problem

% Initializing parameters and settings
T_init = 1.0;       % Initial temperature
T_min =  1e-10;     % Finial stopping temperature
F_min = -1e+100;    % Min value of the function
max_rej=500;        % Maximum number of rejections
max_run=150;        % Maximum number of runs
max_accept = 50;    % Maximum number of accept
initial_search=500; % Initial search period
k = 1;              % Boltzmann constant
Enorm=1e-5;         % Energy norm (eg, Enorm=1e-8)

% Initializing the counters i,j etc
i= 0; j = 0; accept = 0; totaleval = 0;
% Initializing various values
T = T_init;
E_init = Fun(u0);
E_old = E_init; E_new=E_old;
best=u0;  % initially guessed values
% Starting the simulated annealing
while ((T > T_min) & (j <= max_rej) & E_new>F_min)
    i = i+1;
    % Check if max numbers of run/accept are met
    if (i >= max_run) | (accept >= max_accept)
        % reset the counters
        i = 1;  accept = 1;
      % Cooling according to a cooling schedule
        T = cooling(alpha,T);
    end

    % Function evaluations at new locations
    if totaleval<initial_search,
        init_flag=1;
        ns=newsolution(u0,Lb,Ub,init_flag);
    else
        init_flag=0;
        ns=newsolution(best,Lb,Ub,init_flag);
    end
      totaleval=totaleval+1;
      E_new = Fun(ns);
    % Decide to accept the new solution
    DeltaE=E_new-E_old;
    % Accept if improved
    if (DeltaE <0)
        best = ns; E_old = E_new;
        accept=accept+1;   j = 0;
    end
    % Accept with a probability if not improved
    if (DeltaE>=0 & exp(-DeltaE/(k*T))>rand );
        best = ns; E_old = E_new;
        accept=accept+1;
    else
        j=j+1;
    end
    % Update the estimated optimal solution
    f_opt=E_old;
end

best_solution=best
fmin=f_opt
N_evaluation=totaleval

%% New solutions
function s=newsolution(u0,Lb,Ub,init_flag)
  % Either search around
if length(Lb)>0 & init_flag==1,
  s=Lb+(Ub-Lb).*rand(size(u0));
else
  % Or local search by random walk
  stepsize=0.01;
  s=u0+stepsize*(Ub-Lb).*randn(size(u0));
end

s=bounds(s,Lb,Ub);

%% Cooling
function T=cooling(alpha,T)
T=alpha*T;

function ns=bounds(ns,Lb,Ub)
if length(Lb)>0,
% Apply the lower bound
  ns_tmp=ns;
  I=ns_tmp<Lb;
  ns_tmp(I)=Lb(I);
  % Apply the upper bounds
  J=ns_tmp>Ub;
  ns_tmp(J)=Ub(J);
% Update this new move
  ns=ns_tmp;
else
  ns=ns;
end

% d-dimensional objective function
function z=Fun(u)

% Objective
z=fobj(u);

% Apply nonlinear constraints by penalty method
% Z=f+sum_k=1^N lam_k g_k^2 *H(g_k)
z=z+getnonlinear(u);

function Z=getnonlinear(u)
Z=0;
% Penalty constant
lam=10^15; lameq=10^15;
[g,geq]=constraints(u);

% Inequality constraints
for k=1:length(g),
    Z=Z+ lam*g(k)^2*getH(g(k));
end

% Equality constraints (when geq=[], length->0)
for k=1:length(geq),
   Z=Z+lameq*geq(k)^2*geteqH(geq(k));
end

% Test if inequalities hold
function H=getH(g)
if g<=0,
    H=0;
else
    H=1;
end

% Test if equalities hold
function H=geteqH(g)
if g==0,
    H=0;
else
    H=1;
end

% Objective functions
function z=fobj(u)
% Welded beam design optimization
z=1.10471*u(1)^2*u(2)+0.04811*u(3)*u(4)*(14.0+u(2));

% All constraints
function [g,geq]=constraints(x)
% Inequality constraints
Q=6000*(14+x(2)/2);
D=sqrt(x(2)^2/4+(x(1)+x(3))^2/4);
J=2*(x(1)*x(2)*sqrt(2)*(x(2)^2/12+(x(1)+x(3))^2/4));
alpha=6000/(sqrt(2)*x(1)*x(2));
beta=Q*D/J;
tau=sqrt(alpha^2+2*alpha*beta*x(2)/(2*D)+beta^2);
sigma=504000/(x(4)*x(3)^2);
delta=65856000/(30*10^6*x(4)*x(3)^3);
tmpf=4.013*(30*10^6)/196;
P=tmpf*sqrt(x(3)^2*x(4)^6/36)*(1-x(3)*sqrt(30/48)/28);

g(1)=tau-13600;
g(2)=sigma-30000;
g(3)=x(1)-x(4);
g(4)=0.10471*x(1)^2+0.04811*x(3)*x(4)*(14+x(2))-5.0;
g(5)=0.125-x(1);
g(6)=delta-0.25;
g(7)=6000-P;

% Equality constraints
geq=[];
%% End of the program --------------------------------


