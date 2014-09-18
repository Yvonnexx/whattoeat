var StringUtils = (function () {
    var stringUtils = {};
                    
    stringUtils.string_inject = function(sSource, aValues) {
        var i = 0;
        
        if (aValues && aValues.length) {
                return sSource.replace(/\{\d+\}/g, function(substr) {
                var sValue = aValues[i];

                if (sValue) {
                    i += 1;
                    return sValue;
                }
                else {
                    return substr;
                }
            })
        }
        return sSource;
    };

    return stringUtils;
})();