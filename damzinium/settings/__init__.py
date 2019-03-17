from damzinium.env import DAMZINIUM_ENV

if DAMZINIUM_ENV in ('development', 'staging', 'production'):
	exec(f'from .{DAMZINIUM_ENV} import *')
