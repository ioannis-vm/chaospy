"""Frontend collection."""
import inspect
import numpy

from .clenshaw_curtis import quad_clenshaw_curtis
from .gauss_patterson import quad_gauss_patterson
from .gauss_legendre import quad_gauss_legendre
from .genz_keister import quad_genz_keister
from .golub_welsch import quad_golub_welsch
from .leja import quad_leja
from .fejer import quad_fejer

QUAD_FUNCTIONS = {
    "clenshaw_curtis": quad_clenshaw_curtis,
    "gauss_legendre": quad_gauss_legendre,
    "gauss_patterson": quad_gauss_patterson,
    "genz_keister": quad_genz_keister,
    "golub_welsch": quad_golub_welsch,
    "leja": quad_leja,
    "fejer": quad_fejer,
}

QUAD_SHORT_NAMES = {
    "c": "clenshaw_curtis",
    "e": "gauss_legendre",
    "p": "gauss_patterson",
    "z": "genz_keister",
    "g": "golub_welsch",
    "j": "leja",
    "f": "fejer",
}



def get_function(rule, domain, **parameters):
    """
    Create a quadrature function and set default parameter values.

    Args:
        rule (str) : Name of quadrature rule defined in `QUAD_FUNCTIONS`.
        domain (Dist, numpy.ndarray) : Defines `lower` and `upper` that is passed
            quadrature rule. If `Dist`, `domain` is renamed to `dist` and also
            passed.
        **parameters (optional) : Redefining of the parameter defaults. Only
            add parameters that the quadrature rule expect.
    Returns:
        (callable) : Function that can be called only using argument `order`.
    """
    from ...distributions.baseclass import Dist
    if isinstance(domain, Dist):
        lower, upper = domain.range()
        parameters["dist"] = domain
    else:
        lower, upper = numpy.array(domain)
    parameters["lower"] = lower
    parameters["upper"] = upper

    quad_function = QUAD_FUNCTIONS[rule]
    parameters_spec = inspect.getargspec(quad_function)[0]
    parameters_spec = {key: None for key in parameters_spec}
    del parameters_spec["order"]

    for key in parameters_spec:
        if key in parameters:
            parameters_spec[key] = parameters[key]

    def _quad_function(order, *args, **kws):
        """Implementation of quadrature function."""
        params = parameters_spec.copy()
        params.update(kws)
        return quad_function(order, *args, **params)

    return _quad_function
