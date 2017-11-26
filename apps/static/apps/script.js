var token = 'eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.Drwkr9NTeSetTmC4j-ZaRx4QoZYAa1jEfolMq6EFiKtarKfixIvemorhFU0oHGEezLeZk6MWusdxiWXgihZxFcWE-92RWjah.1_Ot-vgXI-uizPfzbwHnbg.3U_yTUSzY1xr4Bv_gg0BVZOq-UNdLAaC5VxUa_1Klu3cptX1XjWv00krprOISL6382aCFV6sMBYjCUltsom-eSfzObv_0qvBQDzLT5MLD7JT-TBhTlKqT3an6bQRDMBP3CTCbn4jpMT_HuWOteHkEbFGVcC2SWROj1sa04tqoFJ0ZXuOeUVYf0rz_lWM4TofqOqvQ3GRDw2VW4i-1WG-v_lAElQMKCEuFXBZFRekvHdH2Qp_fmV5jEKjqXH0PbkoC7TJKOYh3QYTIG2W3IJRutI3Bh2IYID1qk0NhOmOUEm2-I7BzjKQtJxCJDVTmZaDLm1siWFgCl-j6WNyb9ik2_fCzsHqrXBJoCAu9P8De2Zasybr9cAFGWl_-8VFyxSEENarF607XjpijJNrT-NGEQ8Enkzin5XkynSdsz_PZgz09N1kmjA5VDNUTCwlRNeow3wNEkmIXUmXcBDkN2ThQ1nERNa9V8AdzouPlmiceQjyLOELTMaXcFSKSVLh-fP_jIYtClDahC3tXjkelmmBjA.dxJ-nQprZpw1rRPECFImTwPmaxwWYj0kpJNpEd98YYg'

$(document).ready(function()
{
    $.ajaxSetup({
        headers:
        { 
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'),
            'Authorization': token,
            'Content-Type':'application/json'
        }
    });
});