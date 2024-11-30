/**
* jQuery.UI.iPad plugin
* Copyright (c) 2010 Stephen von Takach
* licensed under MIT.
* Date: 27/8/2010
*
* Project Home: 
* http://code.google.com/p/jquery-ui-for-ipad-and-iphone/
*
* Modified: 19/01/2012 
* Organized as a proper plugin and added addTouch()
*/

(function($) {
	
	var lastTap = null;				// Holds last tapped element (so we can compare for double tap)
	var tapValid = false;			// Are we still in the .6 second window where a double tap can occur
	var tapTimeout = null;			// The timeout reference
	var rightClickPending = false;	// Is a right click still feasible
	var rightClickEvent = null;		// the original event
	var holdTimeout = null;			// timeout reference
	var cancelMouseUp = false;		// prevents a click from occuring as we want the context menu

	function cancelTap() {
		tapValid = false;
	};
	
	function cancelHold() {
		if (rightClickPending) {
			window.clearTimeout(holdTimeout);
			rightClickPending = false;
			rightClickEvent = null;
		}
	};

	function startHold(event) {
		if (rightClickPending)
			return;

		rightClickPending = true; // We could be performing a right click
		rightClickEvent = (event.changedTouches)[0];
		holdTimeout = window.setTimeout("doRightClick();", 800);
	};

	function doRightClick() {
		rightClickPending = false;

		// We need to mouse up (as we were down)
		var first = rightClickEvent,
			simulatedEvent = document.createEvent("MouseEvent");
		simulatedEvent.initMouseEvent("mouseup", true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
				false, false, false, false, 0, null);
		first.target.dispatchEvent(simulatedEvent);

		// Emulate a right click
		simulatedEvent = document.createEvent("MouseEvent");
		simulatedEvent.initMouseEvent("mousedown", true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
				false, false, false, false, 2, null);
		first.target.dispatchEvent(simulatedEvent);

		// Show a context menu
		simulatedEvent = document.createEvent("MouseEvent");
		simulatedEvent.initMouseEvent("contextmenu", true, true, window, 1, first.screenX + 50, first.screenY + 5, first.clientX + 50, first.clientY + 5,
	                                  false, false, false, false, 2, null);
		first.target.dispatchEvent(simulatedEvent);

		// Note: I don't mouse up the right click here however feel free to add if required
		cancelMouseUp = true;
		rightClickEvent = null; // Release memory
	};

	// mouse over event then mouse down
	function iPadTouchStart(event) {
		var touches = event.changedTouches,
			first = touches[0],
			type = "mouseover",
			simulatedEvent = document.createEvent("MouseEvent");

		// Mouse over first - I have live events attached on mouse over
		simulatedEvent.initMouseEvent(type, true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                            false, false, false, false, 0, null);
		first.target.dispatchEvent(simulatedEvent);

		type = "mousedown";
		simulatedEvent = document.createEvent("MouseEvent");

		simulatedEvent.initMouseEvent(type, true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                            false, false, false, false, 0, null);
		first.target.dispatchEvent(simulatedEvent);


		if (!tapValid) {
			lastTap = first.target;
			tapValid = true;
			tapTimeout = window.setTimeout(function() { cancelTap(); }, 600);
			startHold(event);
		}
		else {
			window.clearTimeout(tapTimeout);

			// If a double tap is still a possibility and the elements are the same then perform a double click
			if (first.target == lastTap) {
				lastTap = null;
				tapValid = false;

				type = "click";
				simulatedEvent = document.createEvent("MouseEvent");

				simulatedEvent.initMouseEvent(type, true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                         	false, false, false, false, 0/*left*/, null);
				first.target.dispatchEvent(simulatedEvent);

				type = "dblclick";
				simulatedEvent = document.createEvent("MouseEvent");

				simulatedEvent.initMouseEvent(type, true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                         	false, false, false, false, 0/*left*/, null);
				first.target.dispatchEvent(simulatedEvent);
			}
			else {
				lastTap = first.target;
				tapValid = true;
				tapTimeout = window.setTimeout(function() { cancelTap(); }, 600);
				startHold(event);
			}
		}
	};

	function iPadTouchHandler(event) {
		
		var type = "",
			button = 0; /*left*/

		if (event.touches.length > 1)
			return;

		switch (event.type) {
			case "touchstart":
				if ($(event.changedTouches[0].target).is("select")) {
					return;
				}
				iPadTouchStart(event); /*We need to trigger two events here to support one touch drag and drop*/
				event.preventDefault();
				return false;
				break;

			case "touchmove":
				cancelHold();
				type = "mousemove";
				event.preventDefault();
				break;

			case "touchend":
				if (cancelMouseUp) {
					cancelMouseUp = false;
					event.preventDefault();
					return false;
				}
				cancelHold();
				type = "mouseup";
				break;

			default:
				return;
		}

		var touches = event.changedTouches,
			first = touches[0],
			simulatedEvent = document.createEvent("MouseEvent");

		simulatedEvent.initMouseEvent(type, true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                            false, false, false, false, button, null);

		first.target.dispatchEvent(simulatedEvent);

		if (type == "mouseup" && tapValid && first.target == lastTap) {	// This actually emulates the ipads default behaviour (which we prevented)
			simulatedEvent = document.createEvent("MouseEvent");		// This check avoids click being emulated on a double tap

			simulatedEvent.initMouseEvent("click", true, true, window, 1, first.screenX, first.screenY, first.clientX, first.clientY,
	                            false, false, false, false, button, null);

			first.target.dispatchEvent(simulatedEvent);
		}
	};
	
	$.extend($.support, {
		touch: "ontouchend" in document
	});

	$.fn.addTouch = function() {
	    if ($.support.touch) {
            this.each(function(i,el){
                el.addEventListener("touchstart", iPadTouchHandler, false);
                el.addEventListener("touchmove", iPadTouchHandler, false);
                el.addEventListener("touchend", iPadTouchHandler, false);
                el.addEventListener("touchcancel", iPadTouchHandler, false);
            });
	    }
	};

	$.fn.addTouchLive = function(selector) {
		if ($.support.touch) {
			this.each(function(i,el){
                $(el).on("touchstart", selector, function(e) {
                	iPadTouchHandler(e.originalEvent);
                });
                $(el).on("touchmove", selector, function(e) {
                	iPadTouchHandler(e.originalEvent);
                });
                $(el).on("touchend", selector, function(e) {
                	iPadTouchHandler(e.originalEvent);
                });
                $(el).on("touchcancel", selector, function(e) {
                	iPadTouchHandler(e.originalEvent);
                });
            });
		}
	}

})(jQuery);
// From http://baagoe.com/en/RandomMusings/javascript/
// Johannes BaagÌüe <baagoe@baagoe.com>, 2010
function Mash() {
  var n = 0xefc8249d;

  var mash = function(data) {
    data = data.toString();
    for (var i = 0; i < data.length; i++) {
      n += data.charCodeAt(i);
      var h = 0.02519603282416938 * n;
      n = h >>> 0;
      h -= n;
      h *= n;
      n = h >>> 0;
      h -= n;
      n += h * 0x100000000; // 2^32
    }
    return (n >>> 0) * 2.3283064365386963e-10; // 2^-32
  };

  mash.version = 'Mash 0.9';
  return mash;
}

// From http://baagoe.com/en/RandomMusings/javascript/
function Alea() {
  var MAX_INT = Math.pow(2,32) - 1;
	
  this.next = function(args) {
    // Johannes BaagÌüe <baagoe@baagoe.com>, 2010
    var s0 = 0;
    var s1 = 0;
    var s2 = 0;
    var c = 1;

    if (args.length == 0) {
      args = [+new Date()];
    }
    var mash = Mash();
    s0 = mash(' ');
    s1 = mash(' ');
    s2 = mash(' ');

    for (var i = 0; i < args.length; i++) {
      s0 -= mash(args[i]);
      if (s0 < 0) {
        s0 += 1;
      }
      s1 -= mash(args[i]);
      if (s1 < 0) {
        s1 += 1;
      }
      s2 -= mash(args[i]);
      if (s2 < 0) {
        s2 += 1;
      }
    }
    mash = null;

    var random = function() {
      var t = 2091639 * s0 + c * 2.3283064365386963e-10; // 2^-32
      s0 = s1;
      s1 = s2;
      return s2 = t - (c = t | 0);
    };
    random.uint32 = function() {
      return random() * 0x100000000; // 2^32
    };
    random.fract53 = function() {
      return random() + 
        (random() * 0x200000 | 0) * 1.1102230246251565e-16; // 2^-53
    };
    random.version = 'Alea 0.9';
    random.args = args;
    return random;

  } (Array.prototype.slice.call(arguments));
  
  /**
   * Generate a random int between 0 (inclusive) and n (exclusive)
   */
  this.nextInt = function (n) {
	  if (n == undefined) {
		  n = MAX_INT;
	  }
	  return Math.floor(this.next() * n);
  }
  
  return this;
};

// seedrandom.js version 2.0.
// Author: David Bau 4/2/2011
//
// Defines a method Math.seedrandom() that, when called, substitutes
// an explicitly seeded RC4-based algorithm for Math.random().  Also
// supports automatic seeding from local or network sources of entropy.
//
// Usage:
//
//   <script src=http://davidbau.com/encode/seedrandom-min.js></script>
//
//   Math.seedrandom('yipee'); Sets Math.random to a function that is
//                             initialized using the given explicit seed.
//
//   Math.seedrandom();        Sets Math.random to a function that is
//                             seeded using the current time, dom state,
//                             and other accumulated local entropy.
//                             The generated seed string is returned.
//
//   Math.seedrandom('yowza', true);
//                             Seeds using the given explicit seed mixed
//                             together with accumulated entropy.
//
//   <script src="http://bit.ly/srandom-512"></script>
//                             Seeds using physical random bits downloaded
//                             from random.org.
//
//   <script src="https://jsonlib.appspot.com/urandom?callback=Math.seedrandom">
//   </script>                 Seeds using urandom bits from call.jsonlib.com,
//                             which is faster than random.org.
//
// Examples:
//
//   Math.seedrandom("hello");            // Use "hello" as the seed.
//   document.write(Math.random());       // Always 0.5463663768140734
//   document.write(Math.random());       // Always 0.43973793770592234
//   var rng1 = Math.random;              // Remember the current prng.
//
//   var autoseed = Math.seedrandom();    // New prng with an automatic seed.
//   document.write(Math.random());       // Pretty much unpredictable.
//
//   Math.random = rng1;                  // Continue "hello" prng sequence.
//   document.write(Math.random());       // Always 0.554769432473455
//
//   Math.seedrandom(autoseed);           // Restart at the previous seed.
//   document.write(Math.random());       // Repeat the 'unpredictable' value.
//
// Notes:
//
// Each time seedrandom('arg') is called, entropy from the passed seed
// is accumulated in a pool to help generate future seeds for the
// zero-argument form of Math.seedrandom, so entropy can be injected over
// time by calling seedrandom with explicit data repeatedly.
//
// On speed - This javascript implementation of Math.random() is about
// 3-10x slower than the built-in Math.random() because it is not native
// code, but this is typically fast enough anyway.  Seeding is more expensive,
// especially if you use auto-seeding.  Some details (timings on Chrome 4):
//
// Our Math.random()            - avg less than 0.002 milliseconds per call
// seedrandom('explicit')       - avg less than 0.5 milliseconds per call
// seedrandom('explicit', true) - avg less than 2 milliseconds per call
// seedrandom()                 - avg about 38 milliseconds per call
//
// LICENSE (BSD):
//
// Copyright 2010 David Bau, all rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
// 
//   1. Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//   2. Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
// 
//   3. Neither the name of this module nor the names of its contributors may
//      be used to endorse or promote products derived from this software
//      without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
/**
 * All code is in an anonymous closure to keep the global namespace clean.
 *
 * @param {number=} overflow 
 * @param {number=} startdenom
 */
(function (pool, math, width, chunks, significance, overflow, startdenom) {


//
// seedrandom()
// This is the seedrandom function described above.
//
math['seedrandom'] = function seedrandom(seed, use_entropy) {
  var key = [];
  var arc4;

  // Flatten the seed string or build one from local entropy if needed.
  seed = mixkey(flatten(
    use_entropy ? [seed, pool] :
    arguments.length ? seed :
    [new Date().getTime(), pool, window], 3), key);

  // Use the seed to initialize an ARC4 generator.
  arc4 = new ARC4(key);

  // Mix the randomness into accumulated entropy.
  mixkey(arc4.S, pool);

  // Override Math.random

  // This function returns a random double in [0, 1) that contains
  // randomness in every bit of the mantissa of the IEEE 754 value.

  math['random'] = function random() {  // Closure to return a random double:
    var n = arc4.g(chunks);             // Start with a numerator n < 2 ^ 48
    var d = startdenom;                 //   and denominator d = 2 ^ 48.
    var x = 0;                          //   and no 'extra last byte'.
    while (n < significance) {          // Fill up all significant digits by
      n = (n + x) * width;              //   shifting numerator and
      d *= width;                       //   denominator and generating a
      x = arc4.g(1);                    //   new least-significant-byte.
    }
    while (n >= overflow) {             // To avoid rounding up, before adding
      n /= 2;                           //   last byte, shift everything
      d /= 2;                           //   right using integer math until
      x >>>= 1;                         //   we have exactly the desired bits.
    }
    return (n + x) / d;                 // Form the number within [0, 1).
  };
    
  /*
   * Added by Eric Dalquist, uses the same logic as Java's Math.nextInt(n) to make
   * sure that the random values are evently distributed across the space
   */
  var randomInt = function randomInt(n) {
     
      if (n < 0) {
        throw "n must be non-negative"
      }
      // Determine the number of counts needed to generate a the number, minimum is 1
      var counts = Math.max(Math.ceil(Math.log(n) / Math.log(width)), 1);
      
      // If counts is greater than 6 then maxRand is greater than 2^53 which is the
      // largest safe int in JavaScript. This library cannot generate random ints larger
      // than width^chunks
      if (counts > chunks) {
        throw "n cannot be greater than " + width + "^" + chunks;
      }

      // Calculate the maximum random number possible for the counts
      var maxRnd = Math.pow(width, counts);     

      // Calculate the maximum valid random number to prevent uneven distribution    
      var maxValid = n * Math.floor(maxRnd / n);
      var rnd;
      var pass = 0;
      do {
          rnd = arc4.g(counts);
          pass++;
      } while (rnd >= maxValid && pass < 100);    // Ignore numbers that are outside of the valid range
      
      return rnd % n;
  };

  Math["randomInt"] = randomInt;

  // Return randomInt function?
  return randomInt;
};

//
// ARC4
//
// An ARC4 implementation.  The constructor takes a key in the form of
// an array of at most (width) integers that should be 0 <= x < (width).
//
// The g(count) method returns a pseudorandom integer that concatenates
// the next (count) outputs from ARC4.  Its return value is a number x
// that is in the range 0 <= x < (width ^ count).
//
/** @constructor */
function ARC4(key) {
  var t, u, me = this, keylen = key.length;
  var i = 0, j = me.i = me.j = me.m = 0;
  me.S = [];
  me.c = [];

  // The empty key [] is treated as [0].
  if (!keylen) { key = [keylen++]; }

  // Set up S using the standard key scheduling algorithm.
  while (i < width) { me.S[i] = i++; }
  for (i = 0; i < width; i++) {
    t = me.S[i];
    j = lowbits(j + t + key[i % keylen]);
    u = me.S[j];
    me.S[i] = u;
    me.S[j] = t;
  }

  // The "g" method returns the next (count) outputs as one number.
  me.g = function getnext(count) {
    var s = me.S;
    var i = lowbits(me.i + 1); var t = s[i];
    var j = lowbits(me.j + t); var u = s[j];
    s[i] = u;
    s[j] = t;
    var r = s[lowbits(t + u)];
    while (--count) {
      i = lowbits(i + 1); t = s[i];
      j = lowbits(j + t); u = s[j];
      s[i] = u;
      s[j] = t;
      r = r * width + s[lowbits(t + u)];
    }
    me.i = i;
    me.j = j;
    return r;
  };
  // For robust unpredictability discard an initial batch of values.
  // See http://www.rsa.com/rsalabs/node.asp?id=2009
  me.g(width);
}

//
// flatten()
// Converts an object tree to nested arrays of strings.
//
/** @param {Object=} result 
  * @param {string=} prop
  * @param {string=} typ */
function flatten(obj, depth, result, prop, typ) {
  result = [];
  typ = typeof(obj);
  if (depth && typ == 'object') {
    for (prop in obj) {
      if (prop.indexOf('S') < 5) {    // Avoid FF3 bug (local/sessionStorage)
        try { result.push(flatten(obj[prop], depth - 1)); } catch (e) {}
      }
    }
  }
  return (result.length ? result : obj + (typ != 'string' ? '\0' : ''));
}

//
// mixkey()
// Mixes a string seed into a key that is an array of integers, and
// returns a shortened string seed that is equivalent to the result key.
//
/** @param {number=} smear 
  * @param {number=} j */
function mixkey(seed, key, smear, j) {
  seed += '';                         // Ensure the seed is a string
  smear = 0;
  for (j = 0; j < seed.length; j++) {
    key[lowbits(j)] =
      lowbits((smear ^= key[lowbits(j)] * 19) + seed.charCodeAt(j));
  }
  seed = '';
  for (j in key) { seed += String.fromCharCode(key[j]); }
  return seed;
}

//
// lowbits()
// A quick "n mod width" for width a power of 2.
//
function lowbits(n) { return n & (width - 1); }

//
// The following constants are related to IEEE 754 limits.
//
startdenom = math.pow(width, chunks);
significance = math.pow(2, significance);
overflow = significance * 2;

//
// When seedrandom.js is loaded, we immediately mix a few bits
// from the built-in RNG into the entropy pool.  Because we do
// not want to intefere with determinstic PRNG state later,
// seedrandom will not call math.random on its own again after
// initialization.
//
mixkey(math.random(), pool);

// End anonymous scope, and pass initial values.
})(
  [],   // pool: entropy pool starts empty
  Math, // math: package containing random, pow, and seedrandom
  256,  // width: each RC4 output is 0 <= x < 256
  6,    // chunks: at least six RC4 outputs for each double
  52    // significance: there are 52 significant digits in a double
);
/*! (c) Tom Wu | http://www-cs-students.stanford.edu/~tjw/jsbn/
 */
var dbits;var canary=244837814094590;var j_lm=((canary&16777215)==15715070);function BigInteger(e,d,f){if(e!=null){if("number"==typeof e){this.fromNumber(e,d,f)}else{if(d==null&&"string"!=typeof e){this.fromString(e,256)}else{this.fromString(e,d)}}}}function nbi(){return new BigInteger(null)}function am1(f,a,b,e,h,g){while(--g>=0){var d=a*this[f++]+b[e]+h;h=Math.floor(d/67108864);b[e++]=d&67108863}return h}function am2(f,q,r,e,o,a){var k=q&32767,p=q>>15;while(--a>=0){var d=this[f]&32767;var g=this[f++]>>15;var b=p*d+g*k;d=k*d+((b&32767)<<15)+r[e]+(o&1073741823);o=(d>>>30)+(b>>>15)+p*g+(o>>>30);r[e++]=d&1073741823}return o}function am3(f,q,r,e,o,a){var k=q&16383,p=q>>14;while(--a>=0){var d=this[f]&16383;var g=this[f++]>>14;var b=p*d+g*k;d=k*d+((b&16383)<<14)+r[e]+o;o=(d>>28)+(b>>14)+p*g;r[e++]=d&268435455}return o}if(j_lm&&(navigator.appName=="Microsoft Internet Explorer")){BigInteger.prototype.am=am2;dbits=30}else{if(j_lm&&(navigator.appName!="Netscape")){BigInteger.prototype.am=am1;dbits=26}else{BigInteger.prototype.am=am3;dbits=28}}BigInteger.prototype.DB=dbits;BigInteger.prototype.DM=((1<<dbits)-1);BigInteger.prototype.DV=(1<<dbits);var BI_FP=52;BigInteger.prototype.FV=Math.pow(2,BI_FP);BigInteger.prototype.F1=BI_FP-dbits;BigInteger.prototype.F2=2*dbits-BI_FP;var BI_RM="0123456789abcdefghijklmnopqrstuvwxyz";var BI_RC=new Array();var rr,vv;rr="0".charCodeAt(0);for(vv=0;vv<=9;++vv){BI_RC[rr++]=vv}rr="a".charCodeAt(0);for(vv=10;vv<36;++vv){BI_RC[rr++]=vv}rr="A".charCodeAt(0);for(vv=10;vv<36;++vv){BI_RC[rr++]=vv}function int2char(a){return BI_RM.charAt(a)}function intAt(b,a){var d=BI_RC[b.charCodeAt(a)];return(d==null)?-1:d}function bnpCopyTo(b){for(var a=this.t-1;a>=0;--a){b[a]=this[a]}b.t=this.t;b.s=this.s}function bnpFromInt(a){this.t=1;this.s=(a<0)?-1:0;if(a>0){this[0]=a}else{if(a<-1){this[0]=a+this.DV}else{this.t=0}}}function nbv(a){var b=nbi();b.fromInt(a);return b}function bnpFromString(h,c){var e;if(c==16){e=4}else{if(c==8){e=3}else{if(c==256){e=8}else{if(c==2){e=1}else{if(c==32){e=5}else{if(c==4){e=2}else{this.fromRadix(h,c);return}}}}}}this.t=0;this.s=0;var g=h.length,d=false,f=0;while(--g>=0){var a=(e==8)?h[g]&255:intAt(h,g);if(a<0){if(h.charAt(g)=="-"){d=true}continue}d=false;if(f==0){this[this.t++]=a}else{if(f+e>this.DB){this[this.t-1]|=(a&((1<<(this.DB-f))-1))<<f;this[this.t++]=(a>>(this.DB-f))}else{this[this.t-1]|=a<<f}}f+=e;if(f>=this.DB){f-=this.DB}}if(e==8&&(h[0]&128)!=0){this.s=-1;if(f>0){this[this.t-1]|=((1<<(this.DB-f))-1)<<f}}this.clamp();if(d){BigInteger.ZERO.subTo(this,this)}}function bnpClamp(){var a=this.s&this.DM;while(this.t>0&&this[this.t-1]==a){--this.t}}function bnToString(c){if(this.s<0){return"-"+this.negate().toString(c)}var e;if(c==16){e=4}else{if(c==8){e=3}else{if(c==2){e=1}else{if(c==32){e=5}else{if(c==4){e=2}else{return this.toRadix(c)}}}}}var g=(1<<e)-1,l,a=false,h="",f=this.t;var j=this.DB-(f*this.DB)%e;if(f-->0){if(j<this.DB&&(l=this[f]>>j)>0){a=true;h=int2char(l)}while(f>=0){if(j<e){l=(this[f]&((1<<j)-1))<<(e-j);l|=this[--f]>>(j+=this.DB-e)}else{l=(this[f]>>(j-=e))&g;if(j<=0){j+=this.DB;--f}}if(l>0){a=true}if(a){h+=int2char(l)}}}return a?h:"0"}function bnNegate(){var a=nbi();BigInteger.ZERO.subTo(this,a);return a}function bnAbs(){return(this.s<0)?this.negate():this}function bnCompareTo(b){var d=this.s-b.s;if(d!=0){return d}var c=this.t;d=c-b.t;if(d!=0){return(this.s<0)?-d:d}while(--c>=0){if((d=this[c]-b[c])!=0){return d}}return 0}function nbits(a){var c=1,b;if((b=a>>>16)!=0){a=b;c+=16}if((b=a>>8)!=0){a=b;c+=8}if((b=a>>4)!=0){a=b;c+=4}if((b=a>>2)!=0){a=b;c+=2}if((b=a>>1)!=0){a=b;c+=1}return c}function bnBitLength(){if(this.t<=0){return 0}return this.DB*(this.t-1)+nbits(this[this.t-1]^(this.s&this.DM))}function bnpDLShiftTo(c,b){var a;for(a=this.t-1;a>=0;--a){b[a+c]=this[a]}for(a=c-1;a>=0;--a){b[a]=0}b.t=this.t+c;b.s=this.s}function bnpDRShiftTo(c,b){for(var a=c;a<this.t;++a){b[a-c]=this[a]}b.t=Math.max(this.t-c,0);b.s=this.s}function bnpLShiftTo(j,e){var b=j%this.DB;var a=this.DB-b;var g=(1<<a)-1;var f=Math.floor(j/this.DB),h=(this.s<<b)&this.DM,d;for(d=this.t-1;d>=0;--d){e[d+f+1]=(this[d]>>a)|h;h=(this[d]&g)<<b}for(d=f-1;d>=0;--d){e[d]=0}e[f]=h;e.t=this.t+f+1;e.s=this.s;e.clamp()}function bnpRShiftTo(g,d){d.s=this.s;var e=Math.floor(g/this.DB);if(e>=this.t){d.t=0;return}var b=g%this.DB;var a=this.DB-b;var f=(1<<b)-1;d[0]=this[e]>>b;for(var c=e+1;c<this.t;++c){d[c-e-1]|=(this[c]&f)<<a;d[c-e]=this[c]>>b}if(b>0){d[this.t-e-1]|=(this.s&f)<<a}d.t=this.t-e;d.clamp()}function bnpSubTo(d,f){var e=0,g=0,b=Math.min(d.t,this.t);while(e<b){g+=this[e]-d[e];f[e++]=g&this.DM;g>>=this.DB}if(d.t<this.t){g-=d.s;while(e<this.t){g+=this[e];f[e++]=g&this.DM;g>>=this.DB}g+=this.s}else{g+=this.s;while(e<d.t){g-=d[e];f[e++]=g&this.DM;g>>=this.DB}g-=d.s}f.s=(g<0)?-1:0;if(g<-1){f[e++]=this.DV+g}else{if(g>0){f[e++]=g}}f.t=e;f.clamp()}function bnpMultiplyTo(c,e){var b=this.abs(),f=c.abs();var d=b.t;e.t=d+f.t;while(--d>=0){e[d]=0}for(d=0;d<f.t;++d){e[d+b.t]=b.am(0,f[d],e,d,0,b.t)}e.s=0;e.clamp();if(this.s!=c.s){BigInteger.ZERO.subTo(e,e)}}function bnpSquareTo(d){var a=this.abs();var b=d.t=2*a.t;while(--b>=0){d[b]=0}for(b=0;b<a.t-1;++b){var e=a.am(b,a[b],d,2*b,0,1);if((d[b+a.t]+=a.am(b+1,2*a[b],d,2*b+1,e,a.t-b-1))>=a.DV){d[b+a.t]-=a.DV;d[b+a.t+1]=1}}if(d.t>0){d[d.t-1]+=a.am(b,a[b],d,2*b,0,1)}d.s=0;d.clamp()}function bnpDivRemTo(n,h,g){var w=n.abs();if(w.t<=0){return}var k=this.abs();if(k.t<w.t){if(h!=null){h.fromInt(0)}if(g!=null){this.copyTo(g)}return}if(g==null){g=nbi()}var d=nbi(),a=this.s,l=n.s;var v=this.DB-nbits(w[w.t-1]);if(v>0){w.lShiftTo(v,d);k.lShiftTo(v,g)}else{w.copyTo(d);k.copyTo(g)}var p=d.t;var b=d[p-1];if(b==0){return}var o=b*(1<<this.F1)+((p>1)?d[p-2]>>this.F2:0);var A=this.FV/o,z=(1<<this.F1)/o,x=1<<this.F2;var u=g.t,s=u-p,f=(h==null)?nbi():h;d.dlShiftTo(s,f);if(g.compareTo(f)>=0){g[g.t++]=1;g.subTo(f,g)}BigInteger.ONE.dlShiftTo(p,f);f.subTo(d,d);while(d.t<p){d[d.t++]=0}while(--s>=0){var c=(g[--u]==b)?this.DM:Math.floor(g[u]*A+(g[u-1]+x)*z);if((g[u]+=d.am(0,c,g,s,0,p))<c){d.dlShiftTo(s,f);g.subTo(f,g);while(g[u]<--c){g.subTo(f,g)}}}if(h!=null){g.drShiftTo(p,h);if(a!=l){BigInteger.ZERO.subTo(h,h)}}g.t=p;g.clamp();if(v>0){g.rShiftTo(v,g)}if(a<0){BigInteger.ZERO.subTo(g,g)}}function bnMod(b){var c=nbi();this.abs().divRemTo(b,null,c);if(this.s<0&&c.compareTo(BigInteger.ZERO)>0){b.subTo(c,c)}return c}function Classic(a){this.m=a}function cConvert(a){if(a.s<0||a.compareTo(this.m)>=0){return a.mod(this.m)}else{return a}}function cRevert(a){return a}function cReduce(a){a.divRemTo(this.m,null,a)}function cMulTo(a,c,b){a.multiplyTo(c,b);this.reduce(b)}function cSqrTo(a,b){a.squareTo(b);this.reduce(b)}Classic.prototype.convert=cConvert;Classic.prototype.revert=cRevert;Classic.prototype.reduce=cReduce;Classic.prototype.mulTo=cMulTo;Classic.prototype.sqrTo=cSqrTo;function bnpInvDigit(){if(this.t<1){return 0}var a=this[0];if((a&1)==0){return 0}var b=a&3;b=(b*(2-(a&15)*b))&15;b=(b*(2-(a&255)*b))&255;b=(b*(2-(((a&65535)*b)&65535)))&65535;b=(b*(2-a*b%this.DV))%this.DV;return(b>0)?this.DV-b:-b}function Montgomery(a){this.m=a;this.mp=a.invDigit();this.mpl=this.mp&32767;this.mph=this.mp>>15;this.um=(1<<(a.DB-15))-1;this.mt2=2*a.t}function montConvert(a){var b=nbi();a.abs().dlShiftTo(this.m.t,b);b.divRemTo(this.m,null,b);if(a.s<0&&b.compareTo(BigInteger.ZERO)>0){this.m.subTo(b,b)}return b}function montRevert(a){var b=nbi();a.copyTo(b);this.reduce(b);return b}function montReduce(a){while(a.t<=this.mt2){a[a.t++]=0}for(var c=0;c<this.m.t;++c){var b=a[c]&32767;var d=(b*this.mpl+(((b*this.mph+(a[c]>>15)*this.mpl)&this.um)<<15))&a.DM;b=c+this.m.t;a[b]+=this.m.am(0,d,a,c,0,this.m.t);while(a[b]>=a.DV){a[b]-=a.DV;a[++b]++}}a.clamp();a.drShiftTo(this.m.t,a);if(a.compareTo(this.m)>=0){a.subTo(this.m,a)}}function montSqrTo(a,b){a.squareTo(b);this.reduce(b)}function montMulTo(a,c,b){a.multiplyTo(c,b);this.reduce(b)}Montgomery.prototype.convert=montConvert;Montgomery.prototype.revert=montRevert;Montgomery.prototype.reduce=montReduce;Montgomery.prototype.mulTo=montMulTo;Montgomery.prototype.sqrTo=montSqrTo;function bnpIsEven(){return((this.t>0)?(this[0]&1):this.s)==0}function bnpExp(h,j){if(h>4294967295||h<1){return BigInteger.ONE}var f=nbi(),a=nbi(),d=j.convert(this),c=nbits(h)-1;d.copyTo(f);while(--c>=0){j.sqrTo(f,a);if((h&(1<<c))>0){j.mulTo(a,d,f)}else{var b=f;f=a;a=b}}return j.revert(f)}function bnModPowInt(b,a){var c;if(b<256||a.isEven()){c=new Classic(a)}else{c=new Montgomery(a)}return this.exp(b,c)}BigInteger.prototype.copyTo=bnpCopyTo;BigInteger.prototype.fromInt=bnpFromInt;BigInteger.prototype.fromString=bnpFromString;BigInteger.prototype.clamp=bnpClamp;BigInteger.prototype.dlShiftTo=bnpDLShiftTo;BigInteger.prototype.drShiftTo=bnpDRShiftTo;BigInteger.prototype.lShiftTo=bnpLShiftTo;BigInteger.prototype.rShiftTo=bnpRShiftTo;BigInteger.prototype.subTo=bnpSubTo;BigInteger.prototype.multiplyTo=bnpMultiplyTo;BigInteger.prototype.squareTo=bnpSquareTo;BigInteger.prototype.divRemTo=bnpDivRemTo;BigInteger.prototype.invDigit=bnpInvDigit;BigInteger.prototype.isEven=bnpIsEven;BigInteger.prototype.exp=bnpExp;BigInteger.prototype.toString=bnToString;BigInteger.prototype.negate=bnNegate;BigInteger.prototype.abs=bnAbs;BigInteger.prototype.compareTo=bnCompareTo;BigInteger.prototype.bitLength=bnBitLength;BigInteger.prototype.mod=bnMod;BigInteger.prototype.modPowInt=bnModPowInt;BigInteger.ZERO=nbv(0);BigInteger.ONE=nbv(1);

/*! (c) Tom Wu | http://www-cs-students.stanford.edu/~tjw/jsbn/
 */
function bnClone(){var a=nbi();this.copyTo(a);return a}function bnIntValue(){if(this.s<0){if(this.t==1){return this[0]-this.DV}else{if(this.t==0){return -1}}}else{if(this.t==1){return this[0]}else{if(this.t==0){return 0}}}return((this[1]&((1<<(32-this.DB))-1))<<this.DB)|this[0]}function bnByteValue(){return(this.t==0)?this.s:(this[0]<<24)>>24}function bnShortValue(){return(this.t==0)?this.s:(this[0]<<16)>>16}function bnpChunkSize(a){return Math.floor(Math.LN2*this.DB/Math.log(a))}function bnSigNum(){if(this.s<0){return -1}else{if(this.t<=0||(this.t==1&&this[0]<=0)){return 0}else{return 1}}}function bnpToRadix(c){if(c==null){c=10}if(this.signum()==0||c<2||c>36){return"0"}var f=this.chunkSize(c);var e=Math.pow(c,f);var i=nbv(e),j=nbi(),h=nbi(),g="";this.divRemTo(i,j,h);while(j.signum()>0){g=(e+h.intValue()).toString(c).substr(1)+g;j.divRemTo(i,j,h)}return h.intValue().toString(c)+g}function bnpFromRadix(m,h){this.fromInt(0);if(h==null){h=10}var f=this.chunkSize(h);var g=Math.pow(h,f),e=false,a=0,l=0;for(var c=0;c<m.length;++c){var k=intAt(m,c);if(k<0){if(m.charAt(c)=="-"&&this.signum()==0){e=true}continue}l=h*l+k;if(++a>=f){this.dMultiply(g);this.dAddOffset(l,0);a=0;l=0}}if(a>0){this.dMultiply(Math.pow(h,a));this.dAddOffset(l,0)}if(e){BigInteger.ZERO.subTo(this,this)}}function bnpFromNumber(f,e,h){if("number"==typeof e){if(f<2){this.fromInt(1)}else{this.fromNumber(f,h);if(!this.testBit(f-1)){this.bitwiseTo(BigInteger.ONE.shiftLeft(f-1),op_or,this)}if(this.isEven()){this.dAddOffset(1,0)}while(!this.isProbablePrime(e)){this.dAddOffset(2,0);if(this.bitLength()>f){this.subTo(BigInteger.ONE.shiftLeft(f-1),this)}}}}else{var d=new Array(),g=f&7;d.length=(f>>3)+1;e.nextBytes(d);if(g>0){d[0]&=((1<<g)-1)}else{d[0]=0}this.fromString(d,256)}}function bnToByteArray(){var b=this.t,c=new Array();c[0]=this.s;var e=this.DB-(b*this.DB)%8,f,a=0;if(b-->0){if(e<this.DB&&(f=this[b]>>e)!=(this.s&this.DM)>>e){c[a++]=f|(this.s<<(this.DB-e))}while(b>=0){if(e<8){f=(this[b]&((1<<e)-1))<<(8-e);f|=this[--b]>>(e+=this.DB-8)}else{f=(this[b]>>(e-=8))&255;if(e<=0){e+=this.DB;--b}}if((f&128)!=0){f|=-256}if(a==0&&(this.s&128)!=(f&128)){++a}if(a>0||f!=this.s){c[a++]=f}}}return c}function bnEquals(b){return(this.compareTo(b)==0)}function bnMin(b){return(this.compareTo(b)<0)?this:b}function bnMax(b){return(this.compareTo(b)>0)?this:b}function bnpBitwiseTo(c,h,e){var d,g,b=Math.min(c.t,this.t);for(d=0;d<b;++d){e[d]=h(this[d],c[d])}if(c.t<this.t){g=c.s&this.DM;for(d=b;d<this.t;++d){e[d]=h(this[d],g)}e.t=this.t}else{g=this.s&this.DM;for(d=b;d<c.t;++d){e[d]=h(g,c[d])}e.t=c.t}e.s=h(this.s,c.s);e.clamp()}function op_and(a,b){return a&b}function bnAnd(b){var c=nbi();this.bitwiseTo(b,op_and,c);return c}function op_or(a,b){return a|b}function bnOr(b){var c=nbi();this.bitwiseTo(b,op_or,c);return c}function op_xor(a,b){return a^b}function bnXor(b){var c=nbi();this.bitwiseTo(b,op_xor,c);return c}function op_andnot(a,b){return a&~b}function bnAndNot(b){var c=nbi();this.bitwiseTo(b,op_andnot,c);return c}function bnNot(){var b=nbi();for(var a=0;a<this.t;++a){b[a]=this.DM&~this[a]}b.t=this.t;b.s=~this.s;return b}function bnShiftLeft(b){var a=nbi();if(b<0){this.rShiftTo(-b,a)}else{this.lShiftTo(b,a)}return a}function bnShiftRight(b){var a=nbi();if(b<0){this.lShiftTo(-b,a)}else{this.rShiftTo(b,a)}return a}function lbit(a){if(a==0){return -1}var b=0;if((a&65535)==0){a>>=16;b+=16}if((a&255)==0){a>>=8;b+=8}if((a&15)==0){a>>=4;b+=4}if((a&3)==0){a>>=2;b+=2}if((a&1)==0){++b}return b}function bnGetLowestSetBit(){for(var a=0;a<this.t;++a){if(this[a]!=0){return a*this.DB+lbit(this[a])}}if(this.s<0){return this.t*this.DB}return -1}function cbit(a){var b=0;while(a!=0){a&=a-1;++b}return b}function bnBitCount(){var c=0,a=this.s&this.DM;for(var b=0;b<this.t;++b){c+=cbit(this[b]^a)}return c}function bnTestBit(b){var a=Math.floor(b/this.DB);if(a>=this.t){return(this.s!=0)}return((this[a]&(1<<(b%this.DB)))!=0)}function bnpChangeBit(c,b){var a=BigInteger.ONE.shiftLeft(c);this.bitwiseTo(a,b,a);return a}function bnSetBit(a){return this.changeBit(a,op_or)}function bnClearBit(a){return this.changeBit(a,op_andnot)}function bnFlipBit(a){return this.changeBit(a,op_xor)}function bnpAddTo(d,f){var e=0,g=0,b=Math.min(d.t,this.t);while(e<b){g+=this[e]+d[e];f[e++]=g&this.DM;g>>=this.DB}if(d.t<this.t){g+=d.s;while(e<this.t){g+=this[e];f[e++]=g&this.DM;g>>=this.DB}g+=this.s}else{g+=this.s;while(e<d.t){g+=d[e];f[e++]=g&this.DM;g>>=this.DB}g+=d.s}f.s=(g<0)?-1:0;if(g>0){f[e++]=g}else{if(g<-1){f[e++]=this.DV+g}}f.t=e;f.clamp()}function bnAdd(b){var c=nbi();this.addTo(b,c);return c}function bnSubtract(b){var c=nbi();this.subTo(b,c);return c}function bnMultiply(b){var c=nbi();this.multiplyTo(b,c);return c}function bnSquare(){var a=nbi();this.squareTo(a);return a}function bnDivide(b){var c=nbi();this.divRemTo(b,c,null);return c}function bnRemainder(b){var c=nbi();this.divRemTo(b,null,c);return c}function bnDivideAndRemainder(b){var d=nbi(),c=nbi();this.divRemTo(b,d,c);return new Array(d,c)}function bnpDMultiply(a){this[this.t]=this.am(0,a-1,this,0,0,this.t);++this.t;this.clamp()}function bnpDAddOffset(b,a){if(b==0){return}while(this.t<=a){this[this.t++]=0}this[a]+=b;while(this[a]>=this.DV){this[a]-=this.DV;if(++a>=this.t){this[this.t++]=0}++this[a]}}function NullExp(){}function nNop(a){return a}function nMulTo(a,c,b){a.multiplyTo(c,b)}function nSqrTo(a,b){a.squareTo(b)}NullExp.prototype.convert=nNop;NullExp.prototype.revert=nNop;NullExp.prototype.mulTo=nMulTo;NullExp.prototype.sqrTo=nSqrTo;function bnPow(a){return this.exp(a,new NullExp())}function bnpMultiplyLowerTo(b,f,e){var d=Math.min(this.t+b.t,f);e.s=0;e.t=d;while(d>0){e[--d]=0}var c;for(c=e.t-this.t;d<c;++d){e[d+this.t]=this.am(0,b[d],e,d,0,this.t)}for(c=Math.min(b.t,f);d<c;++d){this.am(0,b[d],e,d,0,f-d)}e.clamp()}function bnpMultiplyUpperTo(b,e,d){--e;var c=d.t=this.t+b.t-e;d.s=0;while(--c>=0){d[c]=0}for(c=Math.max(e-this.t,0);c<b.t;++c){d[this.t+c-e]=this.am(e-c,b[c],d,0,0,this.t+c-e)}d.clamp();d.drShiftTo(1,d)}function Barrett(a){this.r2=nbi();this.q3=nbi();BigInteger.ONE.dlShiftTo(2*a.t,this.r2);this.mu=this.r2.divide(a);this.m=a}function barrettConvert(a){if(a.s<0||a.t>2*this.m.t){return a.mod(this.m)}else{if(a.compareTo(this.m)<0){return a}else{var b=nbi();a.copyTo(b);this.reduce(b);return b}}}function barrettRevert(a){return a}function barrettReduce(a){a.drShiftTo(this.m.t-1,this.r2);if(a.t>this.m.t+1){a.t=this.m.t+1;a.clamp()}this.mu.multiplyUpperTo(this.r2,this.m.t+1,this.q3);this.m.multiplyLowerTo(this.q3,this.m.t+1,this.r2);while(a.compareTo(this.r2)<0){a.dAddOffset(1,this.m.t+1)}a.subTo(this.r2,a);while(a.compareTo(this.m)>=0){a.subTo(this.m,a)}}function barrettSqrTo(a,b){a.squareTo(b);this.reduce(b)}function barrettMulTo(a,c,b){a.multiplyTo(c,b);this.reduce(b)}Barrett.prototype.convert=barrettConvert;Barrett.prototype.revert=barrettRevert;Barrett.prototype.reduce=barrettReduce;Barrett.prototype.mulTo=barrettMulTo;Barrett.prototype.sqrTo=barrettSqrTo;function bnModPow(q,f){var o=q.bitLength(),h,b=nbv(1),v;if(o<=0){return b}else{if(o<18){h=1}else{if(o<48){h=3}else{if(o<144){h=4}else{if(o<768){h=5}else{h=6}}}}}if(o<8){v=new Classic(f)}else{if(f.isEven()){v=new Barrett(f)}else{v=new Montgomery(f)}}var p=new Array(),d=3,s=h-1,a=(1<<h)-1;p[1]=v.convert(this);if(h>1){var A=nbi();v.sqrTo(p[1],A);while(d<=a){p[d]=nbi();v.mulTo(A,p[d-2],p[d]);d+=2}}var l=q.t-1,x,u=true,c=nbi(),y;o=nbits(q[l])-1;while(l>=0){if(o>=s){x=(q[l]>>(o-s))&a}else{x=(q[l]&((1<<(o+1))-1))<<(s-o);if(l>0){x|=q[l-1]>>(this.DB+o-s)}}d=h;while((x&1)==0){x>>=1;--d}if((o-=d)<0){o+=this.DB;--l}if(u){p[x].copyTo(b);u=false}else{while(d>1){v.sqrTo(b,c);v.sqrTo(c,b);d-=2}if(d>0){v.sqrTo(b,c)}else{y=b;b=c;c=y}v.mulTo(c,p[x],b)}while(l>=0&&(q[l]&(1<<o))==0){v.sqrTo(b,c);y=b;b=c;c=y;if(--o<0){o=this.DB-1;--l}}}return v.revert(b)}function bnGCD(c){var b=(this.s<0)?this.negate():this.clone();var h=(c.s<0)?c.negate():c.clone();if(b.compareTo(h)<0){var e=b;b=h;h=e}var d=b.getLowestSetBit(),f=h.getLowestSetBit();if(f<0){return b}if(d<f){f=d}if(f>0){b.rShiftTo(f,b);h.rShiftTo(f,h)}while(b.signum()>0){if((d=b.getLowestSetBit())>0){b.rShiftTo(d,b)}if((d=h.getLowestSetBit())>0){h.rShiftTo(d,h)}if(b.compareTo(h)>=0){b.subTo(h,b);b.rShiftTo(1,b)}else{h.subTo(b,h);h.rShiftTo(1,h)}}if(f>0){h.lShiftTo(f,h)}return h}function bnpModInt(e){if(e<=0){return 0}var c=this.DV%e,b=(this.s<0)?e-1:0;if(this.t>0){if(c==0){b=this[0]%e}else{for(var a=this.t-1;a>=0;--a){b=(c*b+this[a])%e}}}return b}function bnModInverse(f){var j=f.isEven();if((this.isEven()&&j)||f.signum()==0){return BigInteger.ZERO}var i=f.clone(),h=this.clone();var g=nbv(1),e=nbv(0),l=nbv(0),k=nbv(1);while(i.signum()!=0){while(i.isEven()){i.rShiftTo(1,i);if(j){if(!g.isEven()||!e.isEven()){g.addTo(this,g);e.subTo(f,e)}g.rShiftTo(1,g)}else{if(!e.isEven()){e.subTo(f,e)}}e.rShiftTo(1,e)}while(h.isEven()){h.rShiftTo(1,h);if(j){if(!l.isEven()||!k.isEven()){l.addTo(this,l);k.subTo(f,k)}l.rShiftTo(1,l)}else{if(!k.isEven()){k.subTo(f,k)}}k.rShiftTo(1,k)}if(i.compareTo(h)>=0){i.subTo(h,i);if(j){g.subTo(l,g)}e.subTo(k,e)}else{h.subTo(i,h);if(j){l.subTo(g,l)}k.subTo(e,k)}}if(h.compareTo(BigInteger.ONE)!=0){return BigInteger.ZERO}if(k.compareTo(f)>=0){return k.subtract(f)}if(k.signum()<0){k.addTo(f,k)}else{return k}if(k.signum()<0){return k.add(f)}else{return k}}var lowprimes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997];var lplim=(1<<26)/lowprimes[lowprimes.length-1];function bnIsProbablePrime(e){var d,b=this.abs();if(b.t==1&&b[0]<=lowprimes[lowprimes.length-1]){for(d=0;d<lowprimes.length;++d){if(b[0]==lowprimes[d]){return true}}return false}if(b.isEven()){return false}d=1;while(d<lowprimes.length){var a=lowprimes[d],c=d+1;while(c<lowprimes.length&&a<lplim){a*=lowprimes[c++]}a=b.modInt(a);while(d<c){if(a%lowprimes[d++]==0){return false}}}return b.millerRabin(e)}function bnpMillerRabin(f){var g=this.subtract(BigInteger.ONE);var c=g.getLowestSetBit();if(c<=0){return false}var h=g.shiftRight(c);f=(f+1)>>1;if(f>lowprimes.length){f=lowprimes.length}var b=nbi();for(var e=0;e<f;++e){b.fromInt(lowprimes[Math.floor(Math.random()*lowprimes.length)]);var l=b.modPow(h,this);if(l.compareTo(BigInteger.ONE)!=0&&l.compareTo(g)!=0){var d=1;while(d++<c&&l.compareTo(g)!=0){l=l.modPowInt(2,this);if(l.compareTo(BigInteger.ONE)==0){return false}}if(l.compareTo(g)!=0){return false}}}return true}BigInteger.prototype.chunkSize=bnpChunkSize;BigInteger.prototype.toRadix=bnpToRadix;BigInteger.prototype.fromRadix=bnpFromRadix;BigInteger.prototype.fromNumber=bnpFromNumber;BigInteger.prototype.bitwiseTo=bnpBitwiseTo;BigInteger.prototype.changeBit=bnpChangeBit;BigInteger.prototype.addTo=bnpAddTo;BigInteger.prototype.dMultiply=bnpDMultiply;BigInteger.prototype.dAddOffset=bnpDAddOffset;BigInteger.prototype.multiplyLowerTo=bnpMultiplyLowerTo;BigInteger.prototype.multiplyUpperTo=bnpMultiplyUpperTo;BigInteger.prototype.modInt=bnpModInt;BigInteger.prototype.millerRabin=bnpMillerRabin;BigInteger.prototype.clone=bnClone;BigInteger.prototype.intValue=bnIntValue;BigInteger.prototype.byteValue=bnByteValue;BigInteger.prototype.shortValue=bnShortValue;BigInteger.prototype.signum=bnSigNum;BigInteger.prototype.toByteArray=bnToByteArray;BigInteger.prototype.equals=bnEquals;BigInteger.prototype.min=bnMin;BigInteger.prototype.max=bnMax;BigInteger.prototype.and=bnAnd;BigInteger.prototype.or=bnOr;BigInteger.prototype.xor=bnXor;BigInteger.prototype.andNot=bnAndNot;BigInteger.prototype.not=bnNot;BigInteger.prototype.shiftLeft=bnShiftLeft;BigInteger.prototype.shiftRight=bnShiftRight;BigInteger.prototype.getLowestSetBit=bnGetLowestSetBit;BigInteger.prototype.bitCount=bnBitCount;BigInteger.prototype.testBit=bnTestBit;BigInteger.prototype.setBit=bnSetBit;BigInteger.prototype.clearBit=bnClearBit;BigInteger.prototype.flipBit=bnFlipBit;BigInteger.prototype.add=bnAdd;BigInteger.prototype.subtract=bnSubtract;BigInteger.prototype.multiply=bnMultiply;BigInteger.prototype.divide=bnDivide;BigInteger.prototype.remainder=bnRemainder;BigInteger.prototype.divideAndRemainder=bnDivideAndRemainder;BigInteger.prototype.modPow=bnModPow;BigInteger.prototype.modInverse=bnModInverse;BigInteger.prototype.pow=bnPow;BigInteger.prototype.gcd=bnGCD;BigInteger.prototype.isProbablePrime=bnIsProbablePrime;BigInteger.prototype.square=bnSquare;

/*! (c) Tom Wu | http://www-cs-students.stanford.edu/~tjw/jsbn/
 */
function parseBigInt(b,a){return new BigInteger(b,a)}function linebrk(c,d){var a="";var b=0;while(b+d<c.length){a+=c.substring(b,b+d)+"\n";b+=d}return a+c.substring(b,c.length)}function byte2Hex(a){if(a<16){return"0"+a.toString(16)}else{return a.toString(16)}}function pkcs1pad2(e,h){if(h<e.length+11){alert("Message too long for RSA");return null}var g=new Array();var d=e.length-1;while(d>=0&&h>0){var f=e.charCodeAt(d--);if(f<128){g[--h]=f}else{if((f>127)&&(f<2048)){g[--h]=(f&63)|128;g[--h]=(f>>6)|192}else{g[--h]=(f&63)|128;g[--h]=((f>>6)&63)|128;g[--h]=(f>>12)|224}}}g[--h]=0;var b=new SecureRandom();var a=new Array();while(h>2){a[0]=0;while(a[0]==0){b.nextBytes(a)}g[--h]=a[0]}g[--h]=2;g[--h]=0;return new BigInteger(g)}function oaep_mgf1_arr(c,a,e){var b="",d=0;while(b.length<a){b+=e(String.fromCharCode.apply(String,c.concat([(d&4278190080)>>24,(d&16711680)>>16,(d&65280)>>8,d&255])));d+=1}return b}var SHA1_SIZE=20;function oaep_pad(l,a,c){if(l.length+2*SHA1_SIZE+2>a){throw"Message too long for RSA"}var h="",d;for(d=0;d<a-l.length-2*SHA1_SIZE-2;d+=1){h+="\x00"}var e=rstr_sha1("")+h+"\x01"+l;var f=new Array(SHA1_SIZE);new SecureRandom().nextBytes(f);var g=oaep_mgf1_arr(f,e.length,c||rstr_sha1);var k=[];for(d=0;d<e.length;d+=1){k[d]=e.charCodeAt(d)^g.charCodeAt(d)}var j=oaep_mgf1_arr(k,f.length,rstr_sha1);var b=[0];for(d=0;d<f.length;d+=1){b[d+1]=f[d]^j.charCodeAt(d)}return new BigInteger(b.concat(k))}function RSAKey(){this.n=null;this.e=0;this.d=null;this.p=null;this.q=null;this.dmp1=null;this.dmq1=null;this.coeff=null}function RSASetPublic(b,a){this.isPublic=true;if(typeof b!=="string"){this.n=b;this.e=a}else{if(b!=null&&a!=null&&b.length>0&&a.length>0){this.n=parseBigInt(b,16);this.e=parseInt(a,16)}else{alert("Invalid RSA public key")}}}function RSADoPublic(a){return a.modPowInt(this.e,this.n)}function RSAEncrypt(d){var a=pkcs1pad2(d,(this.n.bitLength()+7)>>3);if(a==null){return null}var e=this.doPublic(a);if(e==null){return null}var b=e.toString(16);if((b.length&1)==0){return b}else{return"0"+b}}function RSAEncryptOAEP(e,d){var a=oaep_pad(e,(this.n.bitLength()+7)>>3,d);if(a==null){return null}var f=this.doPublic(a);if(f==null){return null}var b=f.toString(16);if((b.length&1)==0){return b}else{return"0"+b}}RSAKey.prototype.doPublic=RSADoPublic;RSAKey.prototype.setPublic=RSASetPublic;RSAKey.prototype.encrypt=RSAEncrypt;RSAKey.prototype.encryptOAEP=RSAEncryptOAEP;RSAKey.prototype.type="RSA";

/*! (c) Tom Wu | http://www-cs-students.stanford.edu/~tjw/jsbn/
 */
function pkcs1unpad2(g,j){var a=g.toByteArray();var f=0;while(f<a.length&&a[f]==0){++f}if(a.length-f!=j-1||a[f]!=2){return null}++f;while(a[f]!=0){if(++f>=a.length){return null}}var e="";while(++f<a.length){var h=a[f]&255;if(h<128){e+=String.fromCharCode(h)}else{if((h>191)&&(h<224)){e+=String.fromCharCode(((h&31)<<6)|(a[f+1]&63));++f}else{e+=String.fromCharCode(((h&15)<<12)|((a[f+1]&63)<<6)|(a[f+2]&63));f+=2}}}return e}function oaep_mgf1_str(c,a,e){var b="",d=0;while(b.length<a){b+=e(c+String.fromCharCode.apply(String,[(d&4278190080)>>24,(d&16711680)>>16,(d&65280)>>8,d&255]));d+=1}return b}var SHA1_SIZE=20;function oaep_unpad(l,b,e){l=l.toByteArray();var f;for(f=0;f<l.length;f+=1){l[f]&=255}while(l.length<b){l.unshift(0)}l=String.fromCharCode.apply(String,l);if(l.length<2*SHA1_SIZE+2){throw"Cipher too short"}var c=l.substr(1,SHA1_SIZE);var o=l.substr(SHA1_SIZE+1);var m=oaep_mgf1_str(o,SHA1_SIZE,e||rstr_sha1);var h=[],f;for(f=0;f<c.length;f+=1){h[f]=c.charCodeAt(f)^m.charCodeAt(f)}var j=oaep_mgf1_str(String.fromCharCode.apply(String,h),l.length-SHA1_SIZE,rstr_sha1);var g=[];for(f=0;f<o.length;f+=1){g[f]=o.charCodeAt(f)^j.charCodeAt(f)}g=String.fromCharCode.apply(String,g);if(g.substr(0,SHA1_SIZE)!==rstr_sha1("")){throw"Hash mismatch"}g=g.substr(SHA1_SIZE);var a=g.indexOf("\x01");var k=(a!=-1)?g.substr(0,a).lastIndexOf("\x00"):-1;if(k+1!=a){throw"Malformed data"}return g.substr(a+1)}function RSASetPrivate(c,a,b){this.isPrivate=true;if(typeof c!=="string"){this.n=c;this.e=a;this.d=b}else{if(c!=null&&a!=null&&c.length>0&&a.length>0){this.n=parseBigInt(c,16);this.e=parseInt(a,16);this.d=parseBigInt(b,16)}else{alert("Invalid RSA private key")}}}function RSASetPrivateEx(g,d,e,c,b,a,h,f){this.isPrivate=true;if(g==null){throw"RSASetPrivateEx N == null"}if(d==null){throw"RSASetPrivateEx E == null"}if(g.length==0){throw"RSASetPrivateEx N.length == 0"}if(d.length==0){throw"RSASetPrivateEx E.length == 0"}if(g!=null&&d!=null&&g.length>0&&d.length>0){this.n=parseBigInt(g,16);this.e=parseInt(d,16);this.d=parseBigInt(e,16);this.p=parseBigInt(c,16);this.q=parseBigInt(b,16);this.dmp1=parseBigInt(a,16);this.dmq1=parseBigInt(h,16);this.coeff=parseBigInt(f,16)}else{alert("Invalid RSA private key in RSASetPrivateEx")}}function RSAGenerate(b,i){var a=new SecureRandom();var f=b>>1;this.e=parseInt(i,16);var c=new BigInteger(i,16);for(;;){for(;;){this.p=new BigInteger(b-f,1,a);if(this.p.subtract(BigInteger.ONE).gcd(c).compareTo(BigInteger.ONE)==0&&this.p.isProbablePrime(10)){break}}for(;;){this.q=new BigInteger(f,1,a);if(this.q.subtract(BigInteger.ONE).gcd(c).compareTo(BigInteger.ONE)==0&&this.q.isProbablePrime(10)){break}}if(this.p.compareTo(this.q)<=0){var h=this.p;this.p=this.q;this.q=h}var g=this.p.subtract(BigInteger.ONE);var d=this.q.subtract(BigInteger.ONE);var e=g.multiply(d);if(e.gcd(c).compareTo(BigInteger.ONE)==0){this.n=this.p.multiply(this.q);this.d=c.modInverse(e);this.dmp1=this.d.mod(g);this.dmq1=this.d.mod(d);this.coeff=this.q.modInverse(this.p);break}}}function RSADoPrivate(a){if(this.p==null||this.q==null){return a.modPow(this.d,this.n)}var c=a.mod(this.p).modPow(this.dmp1,this.p);var b=a.mod(this.q).modPow(this.dmq1,this.q);while(c.compareTo(b)<0){c=c.add(this.p)}return c.subtract(b).multiply(this.coeff).mod(this.p).multiply(this.q).add(b)}function RSADecrypt(b){var d=parseBigInt(b,16);var a=this.doPrivate(d);if(a==null){return null}return pkcs1unpad2(a,(this.n.bitLength()+7)>>3)}function RSADecryptOAEP(d,b){var e=parseBigInt(d,16);var a=this.doPrivate(e);if(a==null){return null}return oaep_unpad(a,(this.n.bitLength()+7)>>3,b)}RSAKey.prototype.doPrivate=RSADoPrivate;RSAKey.prototype.setPrivate=RSASetPrivate;RSAKey.prototype.setPrivateEx=RSASetPrivateEx;RSAKey.prototype.generate=RSAGenerate;RSAKey.prototype.decrypt=RSADecrypt;RSAKey.prototype.decryptOAEP=RSADecryptOAEP;

/*! (c) Tom Wu | http://www-cs-students.stanford.edu/~tjw/jsbn/
 */
var b64map="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var b64pad="=";function hex2b64(d){var b;var e;var a="";for(b=0;b+3<=d.length;b+=3){e=parseInt(d.substring(b,b+3),16);a+=b64map.charAt(e>>6)+b64map.charAt(e&63)}if(b+1==d.length){e=parseInt(d.substring(b,b+1),16);a+=b64map.charAt(e<<2)}else{if(b+2==d.length){e=parseInt(d.substring(b,b+2),16);a+=b64map.charAt(e>>2)+b64map.charAt((e&3)<<4)}}if(b64pad){while((a.length&3)>0){a+=b64pad}}return a}function b64tohex(f){var d="";var e;var b=0;var c;var a;for(e=0;e<f.length;++e){if(f.charAt(e)==b64pad){break}a=b64map.indexOf(f.charAt(e));if(a<0){continue}if(b==0){d+=int2char(a>>2);c=a&3;b=1}else{if(b==1){d+=int2char((c<<2)|(a>>4));c=a&15;b=2}else{if(b==2){d+=int2char(c);d+=int2char(a>>2);c=a&3;b=3}else{d+=int2char((c<<2)|(a>>4));d+=int2char(a&15);b=0}}}}if(b==1){d+=int2char(c<<2)}return d}function b64toBA(e){var d=b64tohex(e);var c;var b=new Array();for(c=0;2*c<d.length;++c){b[c]=parseInt(d.substring(2*c,2*c+2),16)}return b};

/*
CryptoJS v3.1.2
code.google.com/p/crypto-js
(c) 2009-2013 by Jeff Mott. All rights reserved.
code.google.com/p/crypto-js/wiki/License
*/
/**
 * CryptoJS core components.
 */
var CryptoJS = CryptoJS || (function (Math, undefined) {
    /**
     * CryptoJS namespace.
     */
    var C = {};

    /**
     * Library namespace.
     */
    var C_lib = C.lib = {};

    /**
     * Base object for prototypal inheritance.
     */
    var Base = C_lib.Base = (function () {
        function F() {}

        return {
            /**
             * Creates a new object that inherits from this object.
             *
             * @param {Object} overrides Properties to copy into the new object.
             *
             * @return {Object} The new object.
             *
             * @static
             *
             * @example
             *
             *     var MyType = CryptoJS.lib.Base.extend({
             *         field: 'value',
             *
             *         method: function () {
             *         }
             *     });
             */
            extend: function (overrides) {
                // Spawn
                F.prototype = this;
                var subtype = new F();

                // Augment
                if (overrides) {
                    subtype.mixIn(overrides);
                }

                // Create default initializer
                if (!subtype.hasOwnProperty('init')) {
                    subtype.init = function () {
                        subtype.$super.init.apply(this, arguments);
                    };
                }

                // Initializer's prototype is the subtype object
                subtype.init.prototype = subtype;

                // Reference supertype
                subtype.$super = this;

                return subtype;
            },

            /**
             * Extends this object and runs the init method.
             * Arguments to create() will be passed to init().
             *
             * @return {Object} The new object.
             *
             * @static
             *
             * @example
             *
             *     var instance = MyType.create();
             */
            create: function () {
                var instance = this.extend();
                instance.init.apply(instance, arguments);

                return instance;
            },

            /**
             * Initializes a newly created object.
             * Override this method to add some logic when your objects are created.
             *
             * @example
             *
             *     var MyType = CryptoJS.lib.Base.extend({
             *         init: function () {
             *             // ...
             *         }
             *     });
             */
            init: function () {
            },

            /**
             * Copies properties into this object.
             *
             * @param {Object} properties The properties to mix in.
             *
             * @example
             *
             *     MyType.mixIn({
             *         field: 'value'
             *     });
             */
            mixIn: function (properties) {
                for (var propertyName in properties) {
                    if (properties.hasOwnProperty(propertyName)) {
                        this[propertyName] = properties[propertyName];
                    }
                }

                // IE won't copy toString using the loop above
                if (properties.hasOwnProperty('toString')) {
                    this.toString = properties.toString;
                }
            },

            /**
             * Creates a copy of this object.
             *
             * @return {Object} The clone.
             *
             * @example
             *
             *     var clone = instance.clone();
             */
            clone: function () {
                return this.init.prototype.extend(this);
            }
        };
    }());

    /**
     * An array of 32-bit words.
     *
     * @property {Array} words The array of 32-bit words.
     * @property {number} sigBytes The number of significant bytes in this word array.
     */
    var WordArray = C_lib.WordArray = Base.extend({
        /**
         * Initializes a newly created word array.
         *
         * @param {Array} words (Optional) An array of 32-bit words.
         * @param {number} sigBytes (Optional) The number of significant bytes in the words.
         *
         * @example
         *
         *     var wordArray = CryptoJS.lib.WordArray.create();
         *     var wordArray = CryptoJS.lib.WordArray.create([0x00010203, 0x04050607]);
         *     var wordArray = CryptoJS.lib.WordArray.create([0x00010203, 0x04050607], 6);
         */
        init: function (words, sigBytes) {
            words = this.words = words || [];

            if (sigBytes != undefined) {
                this.sigBytes = sigBytes;
            } else {
                this.sigBytes = words.length * 4;
            }
        },

        /**
         * Converts this word array to a string.
         *
         * @param {Encoder} encoder (Optional) The encoding strategy to use. Default: CryptoJS.enc.Hex
         *
         * @return {string} The stringified word array.
         *
         * @example
         *
         *     var string = wordArray + '';
         *     var string = wordArray.toString();
         *     var string = wordArray.toString(CryptoJS.enc.Utf8);
         */
        toString: function (encoder) {
            return (encoder || Hex).stringify(this);
        },

        /**
         * Concatenates a word array to this word array.
         *
         * @param {WordArray} wordArray The word array to append.
         *
         * @return {WordArray} This word array.
         *
         * @example
         *
         *     wordArray1.concat(wordArray2);
         */
        concat: function (wordArray) {
            // Shortcuts
            var thisWords = this.words;
            var thatWords = wordArray.words;
            var thisSigBytes = this.sigBytes;
            var thatSigBytes = wordArray.sigBytes;

            // Clamp excess bits
            this.clamp();

            // Concat
            if (thisSigBytes % 4) {
                // Copy one byte at a time
                for (var i = 0; i < thatSigBytes; i++) {
                    var thatByte = (thatWords[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                    thisWords[(thisSigBytes + i) >>> 2] |= thatByte << (24 - ((thisSigBytes + i) % 4) * 8);
                }
            } else if (thatWords.length > 0xffff) {
                // Copy one word at a time
                for (var i = 0; i < thatSigBytes; i += 4) {
                    thisWords[(thisSigBytes + i) >>> 2] = thatWords[i >>> 2];
                }
            } else {
                // Copy all words at once
                thisWords.push.apply(thisWords, thatWords);
            }
            this.sigBytes += thatSigBytes;

            // Chainable
            return this;
        },

        /**
         * Removes insignificant bits.
         *
         * @example
         *
         *     wordArray.clamp();
         */
        clamp: function () {
            // Shortcuts
            var words = this.words;
            var sigBytes = this.sigBytes;

            // Clamp
            words[sigBytes >>> 2] &= 0xffffffff << (32 - (sigBytes % 4) * 8);
            words.length = Math.ceil(sigBytes / 4);
        },

        /**
         * Creates a copy of this word array.
         *
         * @return {WordArray} The clone.
         *
         * @example
         *
         *     var clone = wordArray.clone();
         */
        clone: function () {
            var clone = Base.clone.call(this);
            clone.words = this.words.slice(0);

            return clone;
        },

        /**
         * Creates a word array filled with random bytes.
         *
         * @param {number} nBytes The number of random bytes to generate.
         *
         * @return {WordArray} The random word array.
         *
         * @static
         *
         * @example
         *
         *     var wordArray = CryptoJS.lib.WordArray.random(16);
         */
        random: function (nBytes) {
            var words = [];
            for (var i = 0; i < nBytes; i += 4) {
                words.push((Math.random() * 0x100000000) | 0);
            }

            return new WordArray.init(words, nBytes);
        }
    });

    /**
     * Encoder namespace.
     */
    var C_enc = C.enc = {};

    /**
     * Hex encoding strategy.
     */
    var Hex = C_enc.Hex = {
        /**
         * Converts a word array to a hex string.
         *
         * @param {WordArray} wordArray The word array.
         *
         * @return {string} The hex string.
         *
         * @static
         *
         * @example
         *
         *     var hexString = CryptoJS.enc.Hex.stringify(wordArray);
         */
        stringify: function (wordArray) {
            // Shortcuts
            var words = wordArray.words;
            var sigBytes = wordArray.sigBytes;

            // Convert
            var hexChars = [];
            for (var i = 0; i < sigBytes; i++) {
                var bite = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                hexChars.push((bite >>> 4).toString(16));
                hexChars.push((bite & 0x0f).toString(16));
            }

            return hexChars.join('');
        },

        /**
         * Converts a hex string to a word array.
         *
         * @param {string} hexStr The hex string.
         *
         * @return {WordArray} The word array.
         *
         * @static
         *
         * @example
         *
         *     var wordArray = CryptoJS.enc.Hex.parse(hexString);
         */
        parse: function (hexStr) {
            // Shortcut
            var hexStrLength = hexStr.length;

            // Convert
            var words = [];
            for (var i = 0; i < hexStrLength; i += 2) {
                words[i >>> 3] |= parseInt(hexStr.substr(i, 2), 16) << (24 - (i % 8) * 4);
            }

            return new WordArray.init(words, hexStrLength / 2);
        }
    };

    /**
     * Latin1 encoding strategy.
     */
    var Latin1 = C_enc.Latin1 = {
        /**
         * Converts a word array to a Latin1 string.
         *
         * @param {WordArray} wordArray The word array.
         *
         * @return {string} The Latin1 string.
         *
         * @static
         *
         * @example
         *
         *     var latin1String = CryptoJS.enc.Latin1.stringify(wordArray);
         */
        stringify: function (wordArray) {
            // Shortcuts
            var words = wordArray.words;
            var sigBytes = wordArray.sigBytes;

            // Convert
            var latin1Chars = [];
            for (var i = 0; i < sigBytes; i++) {
                var bite = (words[i >>> 2] >>> (24 - (i % 4) * 8)) & 0xff;
                latin1Chars.push(String.fromCharCode(bite));
            }

            return latin1Chars.join('');
        },

        /**
         * Converts a Latin1 string to a word array.
         *
         * @param {string} latin1Str The Latin1 string.
         *
         * @return {WordArray} The word array.
         *
         * @static
         *
         * @example
         *
         *     var wordArray = CryptoJS.enc.Latin1.parse(latin1String);
         */
        parse: function (latin1Str) {
            // Shortcut
            var latin1StrLength = latin1Str.length;

            // Convert
            var words = [];
            for (var i = 0; i < latin1StrLength; i++) {
                words[i >>> 2] |= (latin1Str.charCodeAt(i) & 0xff) << (24 - (i % 4) * 8);
            }

            return new WordArray.init(words, latin1StrLength);
        }
    };

    /**
     * UTF-8 encoding strategy.
     */
    var Utf8 = C_enc.Utf8 = {
        /**
         * Converts a word array to a UTF-8 string.
         *
         * @param {WordArray} wordArray The word array.
         *
         * @return {string} The UTF-8 string.
         *
         * @static
         *
         * @example
         *
         *     var utf8String = CryptoJS.enc.Utf8.stringify(wordArray);
         */
        stringify: function (wordArray) {
            try {
                return decodeURIComponent(escape(Latin1.stringify(wordArray)));
            } catch (e) {
                throw new Error('Malformed UTF-8 data');
            }
        },

        /**
         * Converts a UTF-8 string to a word array.
         *
         * @param {string} utf8Str The UTF-8 string.
         *
         * @return {WordArray} The word array.
         *
         * @static
         *
         * @example
         *
         *     var wordArray = CryptoJS.enc.Utf8.parse(utf8String);
         */
        parse: function (utf8Str) {
            return Latin1.parse(unescape(encodeURIComponent(utf8Str)));
        }
    };

    /**
     * Abstract buffered block algorithm template.
     *
     * The property blockSize must be implemented in a concrete subtype.
     *
     * @property {number} _minBufferSize The number of blocks that should be kept unprocessed in the buffer. Default: 0
     */
    var BufferedBlockAlgorithm = C_lib.BufferedBlockAlgorithm = Base.extend({
        /**
         * Resets this block algorithm's data buffer to its initial state.
         *
         * @example
         *
         *     bufferedBlockAlgorithm.reset();
         */
        reset: function () {
            // Initial values
            this._data = new WordArray.init();
            this._nDataBytes = 0;
        },

        /**
         * Adds new data to this block algorithm's buffer.
         *
         * @param {WordArray|string} data The data to append. Strings are converted to a WordArray using UTF-8.
         *
         * @example
         *
         *     bufferedBlockAlgorithm._append('data');
         *     bufferedBlockAlgorithm._append(wordArray);
         */
        _append: function (data) {
            // Convert string to WordArray, else assume WordArray already
            if (typeof data == 'string') {
                data = Utf8.parse(data);
            }

            // Append
            this._data.concat(data);
            this._nDataBytes += data.sigBytes;
        },

        /**
         * Processes available data blocks.
         *
         * This method invokes _doProcessBlock(offset), which must be implemented by a concrete subtype.
         *
         * @param {boolean} doFlush Whether all blocks and partial blocks should be processed.
         *
         * @return {WordArray} The processed data.
         *
         * @example
         *
         *     var processedData = bufferedBlockAlgorithm._process();
         *     var processedData = bufferedBlockAlgorithm._process(!!'flush');
         */
        _process: function (doFlush) {
            // Shortcuts
            var data = this._data;
            var dataWords = data.words;
            var dataSigBytes = data.sigBytes;
            var blockSize = this.blockSize;
            var blockSizeBytes = blockSize * 4;

            // Count blocks ready
            var nBlocksReady = dataSigBytes / blockSizeBytes;
            if (doFlush) {
                // Round up to include partial blocks
                nBlocksReady = Math.ceil(nBlocksReady);
            } else {
                // Round down to include only full blocks,
                // less the number of blocks that must remain in the buffer
                nBlocksReady = Math.max((nBlocksReady | 0) - this._minBufferSize, 0);
            }

            // Count words ready
            var nWordsReady = nBlocksReady * blockSize;

            // Count bytes ready
            var nBytesReady = Math.min(nWordsReady * 4, dataSigBytes);

            // Process blocks
            if (nWordsReady) {
                for (var offset = 0; offset < nWordsReady; offset += blockSize) {
                    // Perform concrete-algorithm logic
                    this._doProcessBlock(dataWords, offset);
                }

                // Remove processed words
                var processedWords = dataWords.splice(0, nWordsReady);
                data.sigBytes -= nBytesReady;
            }

            // Return processed words
            return new WordArray.init(processedWords, nBytesReady);
        },

        /**
         * Creates a copy of this object.
         *
         * @return {Object} The clone.
         *
         * @example
         *
         *     var clone = bufferedBlockAlgorithm.clone();
         */
        clone: function () {
            var clone = Base.clone.call(this);
            clone._data = this._data.clone();

            return clone;
        },

        _minBufferSize: 0
    });

    /**
     * Abstract hasher template.
     *
     * @property {number} blockSize The number of 32-bit words this hasher operates on. Default: 16 (512 bits)
     */
    var Hasher = C_lib.Hasher = BufferedBlockAlgorithm.extend({
        /**
         * Configuration options.
         */
        cfg: Base.extend(),

        /**
         * Initializes a newly created hasher.
         *
         * @param {Object} cfg (Optional) The configuration options to use for this hash computation.
         *
         * @example
         *
         *     var hasher = CryptoJS.algo.SHA256.create();
         */
        init: function (cfg) {
            // Apply config defaults
            this.cfg = this.cfg.extend(cfg);

            // Set initial values
            this.reset();
        },

        /**
         * Resets this hasher to its initial state.
         *
         * @example
         *
         *     hasher.reset();
         */
        reset: function () {
            // Reset data buffer
            BufferedBlockAlgorithm.reset.call(this);

            // Perform concrete-hasher logic
            this._doReset();
        },

        /**
         * Updates this hasher with a message.
         *
         * @param {WordArray|string} messageUpdate The message to append.
         *
         * @return {Hasher} This hasher.
         *
         * @example
         *
         *     hasher.update('message');
         *     hasher.update(wordArray);
         */
        update: function (messageUpdate) {
            // Append
            this._append(messageUpdate);

            // Update the hash
            this._process();

            // Chainable
            return this;
        },

        /**
         * Finalizes the hash computation.
         * Note that the finalize operation is effectively a destructive, read-once operation.
         *
         * @param {WordArray|string} messageUpdate (Optional) A final message update.
         *
         * @return {WordArray} The hash.
         *
         * @example
         *
         *     var hash = hasher.finalize();
         *     var hash = hasher.finalize('message');
         *     var hash = hasher.finalize(wordArray);
         */
        finalize: function (messageUpdate) {
            // Final message update
            if (messageUpdate) {
                this._append(messageUpdate);
            }

            // Perform concrete-hasher logic
            var hash = this._doFinalize();

            return hash;
        },

        blockSize: 512/32,

        /**
         * Creates a shortcut function to a hasher's object interface.
         *
         * @param {Hasher} hasher The hasher to create a helper for.
         *
         * @return {Function} The shortcut function.
         *
         * @static
         *
         * @example
         *
         *     var SHA256 = CryptoJS.lib.Hasher._createHelper(CryptoJS.algo.SHA256);
         */
        _createHelper: function (hasher) {
            return function (message, cfg) {
                return new hasher.init(cfg).finalize(message);
            };
        },

        /**
         * Creates a shortcut function to the HMAC's object interface.
         *
         * @param {Hasher} hasher The hasher to use in this HMAC helper.
         *
         * @return {Function} The shortcut function.
         *
         * @static
         *
         * @example
         *
         *     var HmacSHA256 = CryptoJS.lib.Hasher._createHmacHelper(CryptoJS.algo.SHA256);
         */
        _createHmacHelper: function (hasher) {
            return function (message, key) {
                return new C_algo.HMAC.init(hasher, key).finalize(message);
            };
        }
    });

    /**
     * Algorithm namespace.
     */
    var C_algo = C.algo = {};

    return C;
}(Math));

/*
CryptoJS v3.1.2
code.google.com/p/crypto-js
(c) 2009-2013 by Jeff Mott. All rights reserved.
code.google.com/p/crypto-js/wiki/License
*/
(function () {
    // Shortcuts
    var C = CryptoJS;
    var C_lib = C.lib;
    var WordArray = C_lib.WordArray;
    var Hasher = C_lib.Hasher;
    var C_algo = C.algo;

    // Reusable object
    var W = [];

    /**
     * SHA-1 hash algorithm.
     */
    var SHA1 = C_algo.SHA1 = Hasher.extend({
        _doReset: function () {
            this._hash = new WordArray.init([
                0x67452301, 0xefcdab89,
                0x98badcfe, 0x10325476,
                0xc3d2e1f0
            ]);
        },

        _doProcessBlock: function (M, offset) {
            // Shortcut
            var H = this._hash.words;

            // Working variables
            var a = H[0];
            var b = H[1];
            var c = H[2];
            var d = H[3];
            var e = H[4];

            // Computation
            for (var i = 0; i < 80; i++) {
                if (i < 16) {
                    W[i] = M[offset + i] | 0;
                } else {
                    var n = W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16];
                    W[i] = (n << 1) | (n >>> 31);
                }

                var t = ((a << 5) | (a >>> 27)) + e + W[i];
                if (i < 20) {
                    t += ((b & c) | (~b & d)) + 0x5a827999;
                } else if (i < 40) {
                    t += (b ^ c ^ d) + 0x6ed9eba1;
                } else if (i < 60) {
                    t += ((b & c) | (b & d) | (c & d)) - 0x70e44324;
                } else /* if (i < 80) */ {
                    t += (b ^ c ^ d) - 0x359d3e2a;
                }

                e = d;
                d = c;
                c = (b << 30) | (b >>> 2);
                b = a;
                a = t;
            }

            // Intermediate hash value
            H[0] = (H[0] + a) | 0;
            H[1] = (H[1] + b) | 0;
            H[2] = (H[2] + c) | 0;
            H[3] = (H[3] + d) | 0;
            H[4] = (H[4] + e) | 0;
        },

        _doFinalize: function () {
            // Shortcuts
            var data = this._data;
            var dataWords = data.words;

            var nBitsTotal = this._nDataBytes * 8;
            var nBitsLeft = data.sigBytes * 8;

            // Add padding
            dataWords[nBitsLeft >>> 5] |= 0x80 << (24 - nBitsLeft % 32);
            dataWords[(((nBitsLeft + 64) >>> 9) << 4) + 14] = Math.floor(nBitsTotal / 0x100000000);
            dataWords[(((nBitsLeft + 64) >>> 9) << 4) + 15] = nBitsTotal;
            data.sigBytes = dataWords.length * 4;

            // Hash final blocks
            this._process();

            // Return final computed hash
            return this._hash;
        },

        clone: function () {
            var clone = Hasher.clone.call(this);
            clone._hash = this._hash.clone();

            return clone;
        }
    });

    /**
     * Shortcut function to the hasher's object interface.
     *
     * @param {WordArray|string} message The message to hash.
     *
     * @return {WordArray} The hash.
     *
     * @static
     *
     * @example
     *
     *     var hash = CryptoJS.SHA1('message');
     *     var hash = CryptoJS.SHA1(wordArray);
     */
    C.SHA1 = Hasher._createHelper(SHA1);

    /**
     * Shortcut function to the HMAC's object interface.
     *
     * @param {WordArray|string} message The message to hash.
     * @param {WordArray|string} key The secret key.
     *
     * @return {WordArray} The HMAC.
     *
     * @static
     *
     * @example
     *
     *     var hmac = CryptoJS.HmacSHA1(message, key);
     */
    C.HmacSHA1 = Hasher._createHmacHelper(SHA1);
}());

/*! rsapem-1.1.js (c) 2012 Kenji Urushima | kjur.github.com/jsrsasign/license
 */
function _rsapem_pemToBase64(b){var a=b;a=a.replace("-----BEGIN RSA PRIVATE KEY-----","");a=a.replace("-----END RSA PRIVATE KEY-----","");a=a.replace(/[ \n]+/g,"");return a}function _rsapem_getPosArrayOfChildrenFromHex(d){var j=new Array();var k=ASN1HEX.getStartPosOfV_AtObj(d,0);var f=ASN1HEX.getPosOfNextSibling_AtObj(d,k);var h=ASN1HEX.getPosOfNextSibling_AtObj(d,f);var b=ASN1HEX.getPosOfNextSibling_AtObj(d,h);var l=ASN1HEX.getPosOfNextSibling_AtObj(d,b);var e=ASN1HEX.getPosOfNextSibling_AtObj(d,l);var g=ASN1HEX.getPosOfNextSibling_AtObj(d,e);var c=ASN1HEX.getPosOfNextSibling_AtObj(d,g);var i=ASN1HEX.getPosOfNextSibling_AtObj(d,c);j.push(k,f,h,b,l,e,g,c,i);return j}function _rsapem_getHexValueArrayOfChildrenFromHex(i){var o=_rsapem_getPosArrayOfChildrenFromHex(i);var r=ASN1HEX.getHexOfV_AtObj(i,o[0]);var f=ASN1HEX.getHexOfV_AtObj(i,o[1]);var j=ASN1HEX.getHexOfV_AtObj(i,o[2]);var k=ASN1HEX.getHexOfV_AtObj(i,o[3]);var c=ASN1HEX.getHexOfV_AtObj(i,o[4]);var b=ASN1HEX.getHexOfV_AtObj(i,o[5]);var h=ASN1HEX.getHexOfV_AtObj(i,o[6]);var g=ASN1HEX.getHexOfV_AtObj(i,o[7]);var l=ASN1HEX.getHexOfV_AtObj(i,o[8]);var m=new Array();m.push(r,f,j,k,c,b,h,g,l);return m}function _rsapem_readPrivateKeyFromASN1HexString(c){var b=_rsapem_getHexValueArrayOfChildrenFromHex(c);this.setPrivateEx(b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8])}function _rsapem_readPrivateKeyFromPEMString(e){var c=_rsapem_pemToBase64(e);var d=b64tohex(c);var b=_rsapem_getHexValueArrayOfChildrenFromHex(d);this.setPrivateEx(b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8])}RSAKey.prototype.readPrivateKeyFromPEMString=_rsapem_readPrivateKeyFromPEMString;RSAKey.prototype.readPrivateKeyFromASN1HexString=_rsapem_readPrivateKeyFromASN1HexString;

/*! rsasign-1.2.7.js (c) 2012 Kenji Urushima | kjur.github.com/jsrsasign/license
 */
var _RE_HEXDECONLY=new RegExp("");_RE_HEXDECONLY.compile("[^0-9a-f]","gi");function _rsasign_getHexPaddedDigestInfoForString(d,e,a){var b=function(f){return KJUR.crypto.Util.hashString(f,a)};var c=b(d);return KJUR.crypto.Util.getPaddedDigestInfoHex(c,a,e)}function _zeroPaddingOfSignature(e,d){var c="";var a=d/4-e.length;for(var b=0;b<a;b++){c=c+"0"}return c+e}function _rsasign_signString(d,a){var b=function(e){return KJUR.crypto.Util.hashString(e,a)};var c=b(d);return this.signWithMessageHash(c,a)}function _rsasign_signWithMessageHash(e,c){var f=KJUR.crypto.Util.getPaddedDigestInfoHex(e,c,this.n.bitLength());var b=parseBigInt(f,16);var d=this.doPrivate(b);var a=d.toString(16);return _zeroPaddingOfSignature(a,this.n.bitLength())}function _rsasign_signStringWithSHA1(a){return _rsasign_signString.call(this,a,"sha1")}function _rsasign_signStringWithSHA256(a){return _rsasign_signString.call(this,a,"sha256")}function pss_mgf1_str(c,a,e){var b="",d=0;while(b.length<a){b+=hextorstr(e(rstrtohex(c+String.fromCharCode.apply(String,[(d&4278190080)>>24,(d&16711680)>>16,(d&65280)>>8,d&255]))));d+=1}return b}function _rsasign_signStringPSS(e,a,d){var c=function(f){return KJUR.crypto.Util.hashHex(f,a)};var b=c(rstrtohex(e));if(d===undefined){d=-1}return this.signWithMessageHashPSS(b,a,d)}function _rsasign_signWithMessageHashPSS(l,a,k){var b=hextorstr(l);var g=b.length;var m=this.n.bitLength()-1;var c=Math.ceil(m/8);var d;var o=function(i){return KJUR.crypto.Util.hashHex(i,a)};if(k===-1||k===undefined){k=g}else{if(k===-2){k=c-g-2}else{if(k<-2){throw"invalid salt length"}}}if(c<(g+k+2)){throw"data too long"}var f="";if(k>0){f=new Array(k);new SecureRandom().nextBytes(f);f=String.fromCharCode.apply(String,f)}var n=hextorstr(o(rstrtohex("\x00\x00\x00\x00\x00\x00\x00\x00"+b+f)));var j=[];for(d=0;d<c-k-g-2;d+=1){j[d]=0}var e=String.fromCharCode.apply(String,j)+"\x01"+f;var h=pss_mgf1_str(n,e.length,o);var q=[];for(d=0;d<e.length;d+=1){q[d]=e.charCodeAt(d)^h.charCodeAt(d)}var p=(65280>>(8*c-m))&255;q[0]&=~p;for(d=0;d<g;d++){q.push(n.charCodeAt(d))}q.push(188);return _zeroPaddingOfSignature(this.doPrivate(new BigInteger(q)).toString(16),this.n.bitLength())}function _rsasign_getDecryptSignatureBI(a,d,c){var b=new RSAKey();b.setPublic(d,c);var e=b.doPublic(a);return e}function _rsasign_getHexDigestInfoFromSig(a,c,b){var e=_rsasign_getDecryptSignatureBI(a,c,b);var d=e.toString(16).replace(/^1f+00/,"");return d}function _rsasign_getAlgNameAndHashFromHexDisgestInfo(f){for(var e in KJUR.crypto.Util.DIGESTINFOHEAD){var d=KJUR.crypto.Util.DIGESTINFOHEAD[e];var b=d.length;if(f.substring(0,b)==d){var c=[e,f.substring(b)];return c}}return[]}function _rsasign_verifySignatureWithArgs(f,b,g,j){var e=_rsasign_getHexDigestInfoFromSig(b,g,j);var h=_rsasign_getAlgNameAndHashFromHexDisgestInfo(e);if(h.length==0){return false}var d=h[0];var i=h[1];var a=function(k){return KJUR.crypto.Util.hashString(k,d)};var c=a(f);return(i==c)}function _rsasign_verifyHexSignatureForMessage(c,b){var d=parseBigInt(c,16);var a=_rsasign_verifySignatureWithArgs(b,d,this.n.toString(16),this.e.toString(16));return a}function _rsasign_verifyString(f,j){j=j.replace(_RE_HEXDECONLY,"");j=j.replace(/[ \n]+/g,"");var b=parseBigInt(j,16);if(b.bitLength()>this.n.bitLength()){return 0}var i=this.doPublic(b);var e=i.toString(16).replace(/^1f+00/,"");var g=_rsasign_getAlgNameAndHashFromHexDisgestInfo(e);if(g.length==0){return false}var d=g[0];var h=g[1];var a=function(k){return KJUR.crypto.Util.hashString(k,d)};var c=a(f);return(h==c)}function _rsasign_verifyWithMessageHash(e,a){a=a.replace(_RE_HEXDECONLY,"");a=a.replace(/[ \n]+/g,"");var b=parseBigInt(a,16);if(b.bitLength()>this.n.bitLength()){return 0}var h=this.doPublic(b);var g=h.toString(16).replace(/^1f+00/,"");var c=_rsasign_getAlgNameAndHashFromHexDisgestInfo(g);if(c.length==0){return false}var d=c[0];var f=c[1];return(f==e)}function _rsasign_verifyStringPSS(c,b,a,f){var e=function(g){return KJUR.crypto.Util.hashHex(g,a)};var d=e(rstrtohex(c));if(f===undefined){f=-1}return this.verifyWithMessageHashPSS(d,b,a,f)}function _rsasign_verifyWithMessageHashPSS(f,s,l,c){var k=new BigInteger(s,16);if(k.bitLength()>this.n.bitLength()){return false}var r=function(i){return KJUR.crypto.Util.hashHex(i,l)};var j=hextorstr(f);var h=j.length;var g=this.n.bitLength()-1;var m=Math.ceil(g/8);var q;if(c===-1||c===undefined){c=h}else{if(c===-2){c=m-h-2}else{if(c<-2){throw"invalid salt length"}}}if(m<(h+c+2)){throw"data too long"}var a=this.doPublic(k).toByteArray();for(q=0;q<a.length;q+=1){a[q]&=255}while(a.length<m){a.unshift(0)}if(a[m-1]!==188){throw"encoded message does not end in 0xbc"}a=String.fromCharCode.apply(String,a);var d=a.substr(0,m-h-1);var e=a.substr(d.length,h);var p=(65280>>(8*m-g))&255;if((d.charCodeAt(0)&p)!==0){throw"bits beyond keysize not zero"}var n=pss_mgf1_str(e,d.length,r);var o=[];for(q=0;q<d.length;q+=1){o[q]=d.charCodeAt(q)^n.charCodeAt(q)}o[0]&=~p;var b=m-h-c-2;for(q=0;q<b;q+=1){if(o[q]!==0){throw"leftmost octets not zero"}}if(o[b]!==1){throw"0x01 marker not found"}return e===hextorstr(r(rstrtohex("\x00\x00\x00\x00\x00\x00\x00\x00"+j+String.fromCharCode.apply(String,o.slice(-c)))))}RSAKey.prototype.signWithMessageHash=_rsasign_signWithMessageHash;RSAKey.prototype.signString=_rsasign_signString;RSAKey.prototype.signStringWithSHA1=_rsasign_signStringWithSHA1;RSAKey.prototype.signStringWithSHA256=_rsasign_signStringWithSHA256;RSAKey.prototype.sign=_rsasign_signString;RSAKey.prototype.signWithSHA1=_rsasign_signStringWithSHA1;RSAKey.prototype.signWithSHA256=_rsasign_signStringWithSHA256;RSAKey.prototype.signWithMessageHashPSS=_rsasign_signWithMessageHashPSS;RSAKey.prototype.signStringPSS=_rsasign_signStringPSS;RSAKey.prototype.signPSS=_rsasign_signStringPSS;RSAKey.SALT_LEN_HLEN=-1;RSAKey.SALT_LEN_MAX=-2;RSAKey.prototype.verifyWithMessageHash=_rsasign_verifyWithMessageHash;RSAKey.prototype.verifyString=_rsasign_verifyString;RSAKey.prototype.verifyHexSignatureForMessage=_rsasign_verifyHexSignatureForMessage;RSAKey.prototype.verify=_rsasign_verifyString;RSAKey.prototype.verifyHexSignatureForByteArrayMessage=_rsasign_verifyHexSignatureForMessage;RSAKey.prototype.verifyWithMessageHashPSS=_rsasign_verifyWithMessageHashPSS;RSAKey.prototype.verifyStringPSS=_rsasign_verifyStringPSS;RSAKey.prototype.verifyPSS=_rsasign_verifyStringPSS;RSAKey.SALT_LEN_RECOVER=-2;

/*! asn1hex-1.1.4.js (c) 2012-2013 Kenji Urushima | kjur.github.com/jsrsasign/license
 */
var ASN1HEX=new function(){this.getByteLengthOfL_AtObj=function(b,c){if(b.substring(c+2,c+3)!="8"){return 1}var a=parseInt(b.substring(c+3,c+4));if(a==0){return -1}if(0<a&&a<10){return a+1}return -2};this.getHexOfL_AtObj=function(b,c){var a=this.getByteLengthOfL_AtObj(b,c);if(a<1){return""}return b.substring(c+2,c+2+a*2)};this.getIntOfL_AtObj=function(c,d){var b=this.getHexOfL_AtObj(c,d);if(b==""){return -1}var a;if(parseInt(b.substring(0,1))<8){a=new BigInteger(b,16)}else{a=new BigInteger(b.substring(2),16)}return a.intValue()};this.getStartPosOfV_AtObj=function(b,c){var a=this.getByteLengthOfL_AtObj(b,c);if(a<0){return a}return c+(a+1)*2};this.getHexOfV_AtObj=function(c,d){var b=this.getStartPosOfV_AtObj(c,d);var a=this.getIntOfL_AtObj(c,d);return c.substring(b,b+a*2)};this.getHexOfTLV_AtObj=function(c,e){var b=c.substr(e,2);var d=this.getHexOfL_AtObj(c,e);var a=this.getHexOfV_AtObj(c,e);return b+d+a};this.getPosOfNextSibling_AtObj=function(c,d){var b=this.getStartPosOfV_AtObj(c,d);var a=this.getIntOfL_AtObj(c,d);return b+a*2};this.getPosArrayOfChildren_AtObj=function(f,j){var c=new Array();var i=this.getStartPosOfV_AtObj(f,j);c.push(i);var b=this.getIntOfL_AtObj(f,j);var g=i;var d=0;while(1){var e=this.getPosOfNextSibling_AtObj(f,g);if(e==null||(e-i>=(b*2))){break}if(d>=200){break}c.push(e);g=e;d++}return c};this.getNthChildIndex_AtObj=function(d,b,e){var c=this.getPosArrayOfChildren_AtObj(d,b);return c[e]};this.getDecendantIndexByNthList=function(e,d,c){if(c.length==0){return d}var f=c.shift();var b=this.getPosArrayOfChildren_AtObj(e,d);return this.getDecendantIndexByNthList(e,b[f],c)};this.getDecendantHexTLVByNthList=function(d,c,b){var a=this.getDecendantIndexByNthList(d,c,b);return this.getHexOfTLV_AtObj(d,a)};this.getDecendantHexVByNthList=function(d,c,b){var a=this.getDecendantIndexByNthList(d,c,b);return this.getHexOfV_AtObj(d,a)}};ASN1HEX.getVbyList=function(d,c,b,e){var a=this.getDecendantIndexByNthList(d,c,b);if(a===undefined){throw"can't find nthList object"}if(e!==undefined){if(d.substr(a,2)!=e){throw"checking tag doesn't match: "+d.substr(a,2)+"!="+e}}return this.getHexOfV_AtObj(d,a)};

/*! x509-1.1.2.js (c) 2012 Kenji Urushima | kjur.github.com/jsrsasign/license
 */
function X509(){this.subjectPublicKeyRSA=null;this.subjectPublicKeyRSA_hN=null;this.subjectPublicKeyRSA_hE=null;this.hex=null;this.getSerialNumberHex=function(){return ASN1HEX.getDecendantHexVByNthList(this.hex,0,[0,1])};this.getIssuerHex=function(){return ASN1HEX.getDecendantHexTLVByNthList(this.hex,0,[0,3])};this.getIssuerString=function(){return X509.hex2dn(ASN1HEX.getDecendantHexTLVByNthList(this.hex,0,[0,3]))};this.getSubjectHex=function(){return ASN1HEX.getDecendantHexTLVByNthList(this.hex,0,[0,5])};this.getSubjectString=function(){return X509.hex2dn(ASN1HEX.getDecendantHexTLVByNthList(this.hex,0,[0,5]))};this.getNotBefore=function(){var a=ASN1HEX.getDecendantHexVByNthList(this.hex,0,[0,4,0]);a=a.replace(/(..)/g,"%$1");a=decodeURIComponent(a);return a};this.getNotAfter=function(){var a=ASN1HEX.getDecendantHexVByNthList(this.hex,0,[0,4,1]);a=a.replace(/(..)/g,"%$1");a=decodeURIComponent(a);return a};this.readCertPEM=function(c){var e=X509.pemToHex(c);var b=X509.getPublicKeyHexArrayFromCertHex(e);var d=new RSAKey();d.setPublic(b[0],b[1]);this.subjectPublicKeyRSA=d;this.subjectPublicKeyRSA_hN=b[0];this.subjectPublicKeyRSA_hE=b[1];this.hex=e};this.readCertPEMWithoutRSAInit=function(c){var d=X509.pemToHex(c);var b=X509.getPublicKeyHexArrayFromCertHex(d);this.subjectPublicKeyRSA.setPublic(b[0],b[1]);this.subjectPublicKeyRSA_hN=b[0];this.subjectPublicKeyRSA_hE=b[1];this.hex=d}}X509.pemToBase64=function(a){var b=a;b=b.replace("-----BEGIN CERTIFICATE-----","");b=b.replace("-----END CERTIFICATE-----","");b=b.replace(/[ \n]+/g,"");return b};X509.pemToHex=function(a){var c=X509.pemToBase64(a);var b=b64tohex(c);return b};X509.getSubjectPublicKeyPosFromCertHex=function(f){var e=X509.getSubjectPublicKeyInfoPosFromCertHex(f);if(e==-1){return -1}var b=ASN1HEX.getPosArrayOfChildren_AtObj(f,e);if(b.length!=2){return -1}var d=b[1];if(f.substring(d,d+2)!="03"){return -1}var c=ASN1HEX.getStartPosOfV_AtObj(f,d);if(f.substring(c,c+2)!="00"){return -1}return c+2};X509.getSubjectPublicKeyInfoPosFromCertHex=function(d){var c=ASN1HEX.getStartPosOfV_AtObj(d,0);var b=ASN1HEX.getPosArrayOfChildren_AtObj(d,c);if(b.length<1){return -1}if(d.substring(b[0],b[0]+10)=="a003020102"){if(b.length<6){return -1}return b[6]}else{if(b.length<5){return -1}return b[5]}};X509.getPublicKeyHexArrayFromCertHex=function(f){var e=X509.getSubjectPublicKeyPosFromCertHex(f);var b=ASN1HEX.getPosArrayOfChildren_AtObj(f,e);if(b.length!=2){return[]}var d=ASN1HEX.getHexOfV_AtObj(f,b[0]);var c=ASN1HEX.getHexOfV_AtObj(f,b[1]);if(d!=null&&c!=null){return[d,c]}else{return[]}};X509.getHexTbsCertificateFromCert=function(b){var a=ASN1HEX.getStartPosOfV_AtObj(b,0);return a};X509.getPublicKeyHexArrayFromCertPEM=function(c){var d=X509.pemToHex(c);var b=X509.getPublicKeyHexArrayFromCertHex(d);return b};X509.hex2dn=function(e){var f="";var c=ASN1HEX.getPosArrayOfChildren_AtObj(e,0);for(var d=0;d<c.length;d++){var b=ASN1HEX.getHexOfTLV_AtObj(e,c[d]);f=f+"/"+X509.hex2rdn(b)}return f};X509.hex2rdn=function(a){var f=ASN1HEX.getDecendantHexTLVByNthList(a,0,[0,0]);var e=ASN1HEX.getDecendantHexVByNthList(a,0,[0,1]);var c="";try{c=X509.DN_ATTRHEX[f]}catch(b){c=f}e=e.replace(/(..)/g,"%$1");var d=decodeURIComponent(e);return c+"="+d};X509.DN_ATTRHEX={"0603550406":"C","060355040a":"O","060355040b":"OU","0603550403":"CN","0603550405":"SN","0603550408":"ST","0603550407":"L",};X509.getPublicKeyFromCertPEM=function(f){var c=X509.getPublicKeyInfoPropOfCertPEM(f);if(c.algoid=="2a864886f70d010101"){var i=KEYUTIL.parsePublicRawRSAKeyHex(c.keyhex);var j=new RSAKey();j.setPublic(i.n,i.e);return j}else{if(c.algoid=="2a8648ce3d0201"){var e=KJUR.crypto.OID.oidhex2name[c.algparam];var j=new KJUR.crypto.ECDSA({curve:e,info:c.keyhex});j.setPublicKeyHex(c.keyhex);return j}else{if(c.algoid=="2a8648ce380401"){var b=ASN1HEX.getVbyList(c.algparam,0,[0],"02");var a=ASN1HEX.getVbyList(c.algparam,0,[1],"02");var d=ASN1HEX.getVbyList(c.algparam,0,[2],"02");var h=ASN1HEX.getHexOfV_AtObj(c.keyhex,0);h=h.substr(2);var j=new KJUR.crypto.DSA();j.setPublic(new BigInteger(b,16),new BigInteger(a,16),new BigInteger(d,16),new BigInteger(h,16));return j}else{throw"unsupported key"}}}};X509.getPublicKeyInfoPropOfCertPEM=function(e){var c={};c.algparam=null;var g=X509.pemToHex(e);var d=ASN1HEX.getPosArrayOfChildren_AtObj(g,0);if(d.length!=3){throw"malformed X.509 certificate PEM (code:001)"}if(g.substr(d[0],2)!="30"){throw"malformed X.509 certificate PEM (code:002)"}var b=ASN1HEX.getPosArrayOfChildren_AtObj(g,d[0]);if(b.length<7){throw"malformed X.509 certificate PEM (code:003)"}var h=ASN1HEX.getPosArrayOfChildren_AtObj(g,b[6]);if(h.length!=2){throw"malformed X.509 certificate PEM (code:004)"}var f=ASN1HEX.getPosArrayOfChildren_AtObj(g,h[0]);if(f.length!=2){throw"malformed X.509 certificate PEM (code:005)"}c.algoid=ASN1HEX.getHexOfV_AtObj(g,f[0]);if(g.substr(f[1],2)=="06"){c.algparam=ASN1HEX.getHexOfV_AtObj(g,f[1])}else{if(g.substr(f[1],2)=="30"){c.algparam=ASN1HEX.getHexOfTLV_AtObj(g,f[1])}}if(g.substr(h[1],2)!="03"){throw"malformed X.509 certificate PEM (code:006)"}var a=ASN1HEX.getHexOfV_AtObj(g,h[1]);c.keyhex=a.substr(2);return c};

/*! crypto-1.1.5.js (c) 2013 Kenji Urushima | kjur.github.com/jsrsasign/license
 */
if(typeof KJUR=="undefined"||!KJUR){KJUR={}}if(typeof KJUR.crypto=="undefined"||!KJUR.crypto){KJUR.crypto={}}KJUR.crypto.Util=new function(){this.DIGESTINFOHEAD={sha1:"3021300906052b0e03021a05000414",sha224:"302d300d06096086480165030402040500041c",sha256:"3031300d060960864801650304020105000420",sha384:"3041300d060960864801650304020205000430",sha512:"3051300d060960864801650304020305000440",md2:"3020300c06082a864886f70d020205000410",md5:"3020300c06082a864886f70d020505000410",ripemd160:"3021300906052b2403020105000414",};this.DEFAULTPROVIDER={md5:"cryptojs",sha1:"cryptojs",sha224:"cryptojs",sha256:"cryptojs",sha384:"cryptojs",sha512:"cryptojs",ripemd160:"cryptojs",hmacmd5:"cryptojs",hmacsha1:"cryptojs",hmacsha224:"cryptojs",hmacsha256:"cryptojs",hmacsha384:"cryptojs",hmacsha512:"cryptojs",hmacripemd160:"cryptojs",MD5withRSA:"cryptojs/jsrsa",SHA1withRSA:"cryptojs/jsrsa",SHA224withRSA:"cryptojs/jsrsa",SHA256withRSA:"cryptojs/jsrsa",SHA384withRSA:"cryptojs/jsrsa",SHA512withRSA:"cryptojs/jsrsa",RIPEMD160withRSA:"cryptojs/jsrsa",MD5withECDSA:"cryptojs/jsrsa",SHA1withECDSA:"cryptojs/jsrsa",SHA224withECDSA:"cryptojs/jsrsa",SHA256withECDSA:"cryptojs/jsrsa",SHA384withECDSA:"cryptojs/jsrsa",SHA512withECDSA:"cryptojs/jsrsa",RIPEMD160withECDSA:"cryptojs/jsrsa",SHA1withDSA:"cryptojs/jsrsa",SHA224withDSA:"cryptojs/jsrsa",SHA256withDSA:"cryptojs/jsrsa",MD5withRSAandMGF1:"cryptojs/jsrsa",SHA1withRSAandMGF1:"cryptojs/jsrsa",SHA224withRSAandMGF1:"cryptojs/jsrsa",SHA256withRSAandMGF1:"cryptojs/jsrsa",SHA384withRSAandMGF1:"cryptojs/jsrsa",SHA512withRSAandMGF1:"cryptojs/jsrsa",RIPEMD160withRSAandMGF1:"cryptojs/jsrsa",};this.CRYPTOJSMESSAGEDIGESTNAME={md5:"CryptoJS.algo.MD5",sha1:"CryptoJS.algo.SHA1",sha224:"CryptoJS.algo.SHA224",sha256:"CryptoJS.algo.SHA256",sha384:"CryptoJS.algo.SHA384",sha512:"CryptoJS.algo.SHA512",ripemd160:"CryptoJS.algo.RIPEMD160"};this.getDigestInfoHex=function(a,b){if(typeof this.DIGESTINFOHEAD[b]=="undefined"){throw"alg not supported in Util.DIGESTINFOHEAD: "+b}return this.DIGESTINFOHEAD[b]+a};this.getPaddedDigestInfoHex=function(h,a,j){var c=this.getDigestInfoHex(h,a);var d=j/4;if(c.length+22>d){throw"key is too short for SigAlg: keylen="+j+","+a}var b="0001";var k="00"+c;var g="";var l=d-b.length-k.length;for(var f=0;f<l;f+=2){g+="ff"}var e=b+g+k;return e};this.hashString=function(a,c){var b=new KJUR.crypto.MessageDigest({alg:c});return b.digestString(a)};this.hashHex=function(b,c){var a=new KJUR.crypto.MessageDigest({alg:c});return a.digestHex(b)};this.sha1=function(a){var b=new KJUR.crypto.MessageDigest({alg:"sha1",prov:"cryptojs"});return b.digestString(a)};this.sha256=function(a){var b=new KJUR.crypto.MessageDigest({alg:"sha256",prov:"cryptojs"});return b.digestString(a)};this.sha256Hex=function(a){var b=new KJUR.crypto.MessageDigest({alg:"sha256",prov:"cryptojs"});return b.digestHex(a)};this.sha512=function(a){var b=new KJUR.crypto.MessageDigest({alg:"sha512",prov:"cryptojs"});return b.digestString(a)};this.sha512Hex=function(a){var b=new KJUR.crypto.MessageDigest({alg:"sha512",prov:"cryptojs"});return b.digestHex(a)};this.md5=function(a){var b=new KJUR.crypto.MessageDigest({alg:"md5",prov:"cryptojs"});return b.digestString(a)};this.ripemd160=function(a){var b=new KJUR.crypto.MessageDigest({alg:"ripemd160",prov:"cryptojs"});return b.digestString(a)};this.getCryptoJSMDByName=function(a){}};KJUR.crypto.MessageDigest=function(params){var md=null;var algName=null;var provName=null;this.setAlgAndProvider=function(alg,prov){if(alg!=null&&prov===undefined){prov=KJUR.crypto.Util.DEFAULTPROVIDER[alg]}if(":md5:sha1:sha224:sha256:sha384:sha512:ripemd160:".indexOf(alg)!=-1&&prov=="cryptojs"){try{this.md=eval(KJUR.crypto.Util.CRYPTOJSMESSAGEDIGESTNAME[alg]).create()}catch(ex){throw"setAlgAndProvider hash alg set fail alg="+alg+"/"+ex}this.updateString=function(str){this.md.update(str)};this.updateHex=function(hex){var wHex=CryptoJS.enc.Hex.parse(hex);this.md.update(wHex)};this.digest=function(){var hash=this.md.finalize();return hash.toString(CryptoJS.enc.Hex)};this.digestString=function(str){this.updateString(str);return this.digest()};this.digestHex=function(hex){this.updateHex(hex);return this.digest()}}if(":sha256:".indexOf(alg)!=-1&&prov=="sjcl"){try{this.md=new sjcl.hash.sha256()}catch(ex){throw"setAlgAndProvider hash alg set fail alg="+alg+"/"+ex}this.updateString=function(str){this.md.update(str)};this.updateHex=function(hex){var baHex=sjcl.codec.hex.toBits(hex);this.md.update(baHex)};this.digest=function(){var hash=this.md.finalize();return sjcl.codec.hex.fromBits(hash)};this.digestString=function(str){this.updateString(str);return this.digest()};this.digestHex=function(hex){this.updateHex(hex);return this.digest()}}};this.updateString=function(str){throw"updateString(str) not supported for this alg/prov: "+this.algName+"/"+this.provName};this.updateHex=function(hex){throw"updateHex(hex) not supported for this alg/prov: "+this.algName+"/"+this.provName};this.digest=function(){throw"digest() not supported for this alg/prov: "+this.algName+"/"+this.provName};this.digestString=function(str){throw"digestString(str) not supported for this alg/prov: "+this.algName+"/"+this.provName};this.digestHex=function(hex){throw"digestHex(hex) not supported for this alg/prov: "+this.algName+"/"+this.provName};if(params!==undefined){if(params.alg!==undefined){this.algName=params.alg;if(params.prov===undefined){this.provName=KJUR.crypto.Util.DEFAULTPROVIDER[this.algName]}this.setAlgAndProvider(this.algName,this.provName)}}};KJUR.crypto.Mac=function(params){var mac=null;var pass=null;var algName=null;var provName=null;var algProv=null;this.setAlgAndProvider=function(alg,prov){if(alg==null){alg="hmacsha1"}alg=alg.toLowerCase();if(alg.substr(0,4)!="hmac"){throw"setAlgAndProvider unsupported HMAC alg: "+alg}if(prov===undefined){prov=KJUR.crypto.Util.DEFAULTPROVIDER[alg]}this.algProv=alg+"/"+prov;var hashAlg=alg.substr(4);if(":md5:sha1:sha224:sha256:sha384:sha512:ripemd160:".indexOf(hashAlg)!=-1&&prov=="cryptojs"){try{var mdObj=eval(KJUR.crypto.Util.CRYPTOJSMESSAGEDIGESTNAME[hashAlg]);this.mac=CryptoJS.algo.HMAC.create(mdObj,this.pass)}catch(ex){throw"setAlgAndProvider hash alg set fail hashAlg="+hashAlg+"/"+ex}this.updateString=function(str){this.mac.update(str)};this.updateHex=function(hex){var wHex=CryptoJS.enc.Hex.parse(hex);this.mac.update(wHex)};this.doFinal=function(){var hash=this.mac.finalize();return hash.toString(CryptoJS.enc.Hex)};this.doFinalString=function(str){this.updateString(str);return this.doFinal()};this.doFinalHex=function(hex){this.updateHex(hex);return this.doFinal()}}};this.updateString=function(str){throw"updateString(str) not supported for this alg/prov: "+this.algProv};this.updateHex=function(hex){throw"updateHex(hex) not supported for this alg/prov: "+this.algProv};this.doFinal=function(){throw"digest() not supported for this alg/prov: "+this.algProv};this.doFinalString=function(str){throw"digestString(str) not supported for this alg/prov: "+this.algProv};this.doFinalHex=function(hex){throw"digestHex(hex) not supported for this alg/prov: "+this.algProv};if(params!==undefined){if(params.pass!==undefined){this.pass=params.pass}if(params.alg!==undefined){this.algName=params.alg;if(params.prov===undefined){this.provName=KJUR.crypto.Util.DEFAULTPROVIDER[this.algName]}this.setAlgAndProvider(this.algName,this.provName)}}};KJUR.crypto.Signature=function(o){var q=null;var n=null;var r=null;var c=null;var l=null;var d=null;var k=null;var h=null;var p=null;var e=null;var b=-1;var g=null;var j=null;var a=null;var i=null;var f=null;this._setAlgNames=function(){if(this.algName.match(/^(.+)with(.+)$/)){this.mdAlgName=RegExp.$1.toLowerCase();this.pubkeyAlgName=RegExp.$2.toLowerCase()}};this._zeroPaddingOfSignature=function(x,w){var v="";var t=w/4-x.length;for(var u=0;u<t;u++){v=v+"0"}return v+x};this.setAlgAndProvider=function(u,t){this._setAlgNames();if(t!="cryptojs/jsrsa"){throw"provider not supported: "+t}if(":md5:sha1:sha224:sha256:sha384:sha512:ripemd160:".indexOf(this.mdAlgName)!=-1){try{this.md=new KJUR.crypto.MessageDigest({alg:this.mdAlgName})}catch(s){throw"setAlgAndProvider hash alg set fail alg="+this.mdAlgName+"/"+s}this.init=function(w,x){var y=null;try{if(x===undefined){y=KEYUTIL.getKey(w)}else{y=KEYUTIL.getKey(w,x)}}catch(v){throw"init failed:"+v}if(y.isPrivate===true){this.prvKey=y;this.state="SIGN"}else{if(y.isPublic===true){this.pubKey=y;this.state="VERIFY"}else{throw"init failed.:"+y}}};this.initSign=function(v){if(typeof v.ecprvhex=="string"&&typeof v.eccurvename=="string"){this.ecprvhex=v.ecprvhex;this.eccurvename=v.eccurvename}else{this.prvKey=v}this.state="SIGN"};this.initVerifyByPublicKey=function(v){if(typeof v.ecpubhex=="string"&&typeof v.eccurvename=="string"){this.ecpubhex=v.ecpubhex;this.eccurvename=v.eccurvename}else{if(v instanceof KJUR.crypto.ECDSA){this.pubKey=v}else{if(v instanceof RSAKey){this.pubKey=v}}}this.state="VERIFY"};this.initVerifyByCertificatePEM=function(v){var w=new X509();w.readCertPEM(v);this.pubKey=w.subjectPublicKeyRSA;this.state="VERIFY"};this.updateString=function(v){this.md.updateString(v)};this.updateHex=function(v){this.md.updateHex(v)};this.sign=function(){this.sHashHex=this.md.digest();if(typeof this.ecprvhex!="undefined"&&typeof this.eccurvename!="undefined"){var v=new KJUR.crypto.ECDSA({curve:this.eccurvename});this.hSign=v.signHex(this.sHashHex,this.ecprvhex)}else{if(this.pubkeyAlgName=="rsaandmgf1"){this.hSign=this.prvKey.signWithMessageHashPSS(this.sHashHex,this.mdAlgName,this.pssSaltLen)}else{if(this.pubkeyAlgName=="rsa"){this.hSign=this.prvKey.signWithMessageHash(this.sHashHex,this.mdAlgName)}else{if(this.prvKey instanceof KJUR.crypto.ECDSA){this.hSign=this.prvKey.signWithMessageHash(this.sHashHex)}else{if(this.prvKey instanceof KJUR.crypto.DSA){this.hSign=this.prvKey.signWithMessageHash(this.sHashHex)}else{throw"Signature: unsupported public key alg: "+this.pubkeyAlgName}}}}}return this.hSign};this.signString=function(v){this.updateString(v);this.sign()};this.signHex=function(v){this.updateHex(v);this.sign()};this.verify=function(v){this.sHashHex=this.md.digest();if(typeof this.ecpubhex!="undefined"&&typeof this.eccurvename!="undefined"){var w=new KJUR.crypto.ECDSA({curve:this.eccurvename});return w.verifyHex(this.sHashHex,v,this.ecpubhex)}else{if(this.pubkeyAlgName=="rsaandmgf1"){return this.pubKey.verifyWithMessageHashPSS(this.sHashHex,v,this.mdAlgName,this.pssSaltLen)}else{if(this.pubkeyAlgName=="rsa"){return this.pubKey.verifyWithMessageHash(this.sHashHex,v)}else{if(this.pubKey instanceof KJUR.crypto.ECDSA){return this.pubKey.verifyWithMessageHash(this.sHashHex,v)}else{if(this.pubKey instanceof KJUR.crypto.DSA){return this.pubKey.verifyWithMessageHash(this.sHashHex,v)}else{throw"Signature: unsupported public key alg: "+this.pubkeyAlgName}}}}}}}};this.init=function(s,t){throw"init(key, pass) not supported for this alg:prov="+this.algProvName};this.initVerifyByPublicKey=function(s){throw"initVerifyByPublicKey(rsaPubKeyy) not supported for this alg:prov="+this.algProvName};this.initVerifyByCertificatePEM=function(s){throw"initVerifyByCertificatePEM(certPEM) not supported for this alg:prov="+this.algProvName};this.initSign=function(s){throw"initSign(prvKey) not supported for this alg:prov="+this.algProvName};this.updateString=function(s){throw"updateString(str) not supported for this alg:prov="+this.algProvName};this.updateHex=function(s){throw"updateHex(hex) not supported for this alg:prov="+this.algProvName};this.sign=function(){throw"sign() not supported for this alg:prov="+this.algProvName};this.signString=function(s){throw"digestString(str) not supported for this alg:prov="+this.algProvName};this.signHex=function(s){throw"digestHex(hex) not supported for this alg:prov="+this.algProvName};this.verify=function(s){throw"verify(hSigVal) not supported for this alg:prov="+this.algProvName};this.initParams=o;if(o!==undefined){if(o.alg!==undefined){this.algName=o.alg;if(o.prov===undefined){this.provName=KJUR.crypto.Util.DEFAULTPROVIDER[this.algName]}else{this.provName=o.prov}this.algProvName=this.algName+":"+this.provName;this.setAlgAndProvider(this.algName,this.provName);this._setAlgNames()}if(o.psssaltlen!==undefined){this.pssSaltLen=o.psssaltlen}if(o.prvkeypem!==undefined){if(o.prvkeypas!==undefined){throw"both prvkeypem and prvkeypas parameters not supported"}else{try{var q=new RSAKey();q.readPrivateKeyFromPEMString(o.prvkeypem);this.initSign(q)}catch(m){throw"fatal error to load pem private key: "+m}}}}};KJUR.crypto.OID=new function(){this.oidhex2name={"2a864886f70d010101":"rsaEncryption","2a8648ce3d0201":"ecPublicKey","2a8648ce380401":"dsa","2a8648ce3d030107":"secp256r1","2b8104001f":"secp192k1","2b81040021":"secp224r1","2b8104000a":"secp256k1","2b81040023":"secp521r1","2b81040022":"secp384r1","2a8648ce380403":"SHA1withDSA","608648016503040301":"SHA224withDSA","608648016503040302":"SHA256withDSA",}};

//     Underscore.js 1.3.1
//     (c) 2009-2012 Jeremy Ashkenas, DocumentCloud Inc.
//     Underscore is freely distributable under the MIT license.
//     Portions of Underscore are inspired or borrowed from Prototype,
//     Oliver Steele's Functional, and John Resig's Micro-Templating.
//     For all details and documentation:
//     http://documentcloud.github.com/underscore

(function() {

  // Baseline setup
  // --------------

  // Establish the root object, `window` in the browser, or `global` on the server.
  var root = this;

  // Save the previous value of the `_` variable.
  var previousUnderscore = root._;

  // Establish the object that gets returned to break out of a loop iteration.
  var breaker = {};

  // Save bytes in the minified (but not gzipped) version:
  var ArrayProto = Array.prototype, ObjProto = Object.prototype, FuncProto = Function.prototype;

  // Create quick reference variables for speed access to core prototypes.
  var slice            = ArrayProto.slice,
      unshift          = ArrayProto.unshift,
      toString         = ObjProto.toString,
      hasOwnProperty   = ObjProto.hasOwnProperty;

  // All **ECMAScript 5** native function implementations that we hope to use
  // are declared here.
  var
    nativeForEach      = ArrayProto.forEach,
    nativeMap          = ArrayProto.map,
    nativeReduce       = ArrayProto.reduce,
    nativeReduceRight  = ArrayProto.reduceRight,
    nativeFilter       = ArrayProto.filter,
    nativeEvery        = ArrayProto.every,
    nativeSome         = ArrayProto.some,
    nativeIndexOf      = ArrayProto.indexOf,
    nativeLastIndexOf  = ArrayProto.lastIndexOf,
    nativeIsArray      = Array.isArray,
    nativeKeys         = Object.keys,
    nativeBind         = FuncProto.bind;

  // Create a safe reference to the Underscore object for use below.
  var _ = function(obj) { return new wrapper(obj); };

  // Export the Underscore object for **Node.js**, with
  // backwards-compatibility for the old `require()` API. If we're in
  // the browser, add `_` as a global object via a string identifier,
  // for Closure Compiler "advanced" mode.
  if (typeof exports !== 'undefined') {
    if (typeof module !== 'undefined' && module.exports) {
      exports = module.exports = _;
    }
    exports._ = _;
  } else {
    root['_'] = _;
  }

  // Current version.
  _.VERSION = '1.3.1';

  // Collection Functions
  // --------------------

  // The cornerstone, an `each` implementation, aka `forEach`.
  // Handles objects with the built-in `forEach`, arrays, and raw objects.
  // Delegates to **ECMAScript 5**'s native `forEach` if available.
  var each = _.each = _.forEach = function(obj, iterator, context) {
    if (obj == null) return;
    if (nativeForEach && obj.forEach === nativeForEach) {
      obj.forEach(iterator, context);
    } else if (obj.length === +obj.length) {
      for (var i = 0, l = obj.length; i < l; i++) {
        if (i in obj && iterator.call(context, obj[i], i, obj) === breaker) return;
      }
    } else {
      for (var key in obj) {
        if (_.has(obj, key)) {
          if (iterator.call(context, obj[key], key, obj) === breaker) return;
        }
      }
    }
  };

  _.now = Date.now || function() {
    return new Date().getTime();
  };

  // Return the results of applying the iterator to each element.
  // Delegates to **ECMAScript 5**'s native `map` if available.
  _.map = _.collect = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    if (nativeMap && obj.map === nativeMap) return obj.map(iterator, context);
    each(obj, function(value, index, list) {
      results[results.length] = iterator.call(context, value, index, list);
    });
    if (obj.length === +obj.length) results.length = obj.length;
    return results;
  };

  // **Reduce** builds up a single result from a list of values, aka `inject`,
  // or `foldl`. Delegates to **ECMAScript 5**'s native `reduce` if available.
  _.reduce = _.foldl = _.inject = function(obj, iterator, memo, context) {
    var initial = arguments.length > 2;
    if (obj == null) obj = [];
    if (nativeReduce && obj.reduce === nativeReduce) {
      if (context) iterator = _.bind(iterator, context);
      return initial ? obj.reduce(iterator, memo) : obj.reduce(iterator);
    }
    each(obj, function(value, index, list) {
      if (!initial) {
        memo = value;
        initial = true;
      } else {
        memo = iterator.call(context, memo, value, index, list);
      }
    });
    if (!initial) throw new TypeError('Reduce of empty array with no initial value');
    return memo;
  };

  // The right-associative version of reduce, also known as `foldr`.
  // Delegates to **ECMAScript 5**'s native `reduceRight` if available.
  _.reduceRight = _.foldr = function(obj, iterator, memo, context) {
    var initial = arguments.length > 2;
    if (obj == null) obj = [];
    if (nativeReduceRight && obj.reduceRight === nativeReduceRight) {
      if (context) iterator = _.bind(iterator, context);
      return initial ? obj.reduceRight(iterator, memo) : obj.reduceRight(iterator);
    }
    var reversed = _.toArray(obj).reverse();
    if (context && !initial) iterator = _.bind(iterator, context);
    return initial ? _.reduce(reversed, iterator, memo, context) : _.reduce(reversed, iterator);
  };

  // Return the first value which passes a truth test. Aliased as `detect`.
  _.find = _.detect = function(obj, iterator, context) {
    var result;
    any(obj, function(value, index, list) {
      if (iterator.call(context, value, index, list)) {
        result = value;
        return true;
      }
    });
    return result;
  };

  // Return all the elements that pass a truth test.
  // Delegates to **ECMAScript 5**'s native `filter` if available.
  // Aliased as `select`.
  _.filter = _.select = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    if (nativeFilter && obj.filter === nativeFilter) return obj.filter(iterator, context);
    each(obj, function(value, index, list) {
      if (iterator.call(context, value, index, list)) results[results.length] = value;
    });
    return results;
  };

  // Return all the elements for which a truth test fails.
  _.reject = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    each(obj, function(value, index, list) {
      if (!iterator.call(context, value, index, list)) results[results.length] = value;
    });
    return results;
  };

  // Determine whether all of the elements match a truth test.
  // Delegates to **ECMAScript 5**'s native `every` if available.
  // Aliased as `all`.
  _.every = _.all = function(obj, iterator, context) {
    var result = true;
    if (obj == null) return result;
    if (nativeEvery && obj.every === nativeEvery) return obj.every(iterator, context);
    each(obj, function(value, index, list) {
      if (!(result = result && iterator.call(context, value, index, list))) return breaker;
    });
    return result;
  };

  // Determine if at least one element in the object matches a truth test.
  // Delegates to **ECMAScript 5**'s native `some` if available.
  // Aliased as `any`.
  var any = _.some = _.any = function(obj, iterator, context) {
    iterator || (iterator = _.identity);
    var result = false;
    if (obj == null) return result;
    if (nativeSome && obj.some === nativeSome) return obj.some(iterator, context);
    each(obj, function(value, index, list) {
      if (result || (result = iterator.call(context, value, index, list))) return breaker;
    });
    return !!result;
  };

  // Determine if a given value is included in the array or object using `===`.
  // Aliased as `contains`.
  _.include = _.contains = function(obj, target) {
    var found = false;
    if (obj == null) return found;
    if (nativeIndexOf && obj.indexOf === nativeIndexOf) return obj.indexOf(target) != -1;
    found = any(obj, function(value) {
      return value === target;
    });
    return found;
  };

  // Invoke a method (with arguments) on every item in a collection.
  _.invoke = function(obj, method) {
    var args = slice.call(arguments, 2);
    return _.map(obj, function(value) {
      return (_.isFunction(method) ? method || value : value[method]).apply(value, args);
    });
  };

  // Convenience version of a common use case of `map`: fetching a property.
  _.pluck = function(obj, key) {
    return _.map(obj, function(value){ return value[key]; });
  };

  // Return the maximum element or (element-based computation).
  _.max = function(obj, iterator, context) {
    if (!iterator && _.isArray(obj)) return Math.max.apply(Math, obj);
    if (!iterator && _.isEmpty(obj)) return -Infinity;
    var result = {computed : -Infinity};
    each(obj, function(value, index, list) {
      var computed = iterator ? iterator.call(context, value, index, list) : value;
      computed >= result.computed && (result = {value : value, computed : computed});
    });
    return result.value;
  };

  // Return the minimum element (or element-based computation).
  _.min = function(obj, iterator, context) {
    if (!iterator && _.isArray(obj)) return Math.min.apply(Math, obj);
    if (!iterator && _.isEmpty(obj)) return Infinity;
    var result = {computed : Infinity};
    each(obj, function(value, index, list) {
      var computed = iterator ? iterator.call(context, value, index, list) : value;
      computed < result.computed && (result = {value : value, computed : computed});
    });
    return result.value;
  };

  // Shuffle an array.
  _.shuffle = function(obj) {
    var shuffled = [], rand;
    each(obj, function(value, index, list) {
      if (index == 0) {
        shuffled[0] = value;
      } else {
        rand = Math.floor(Math.random() * (index + 1));
        shuffled[index] = shuffled[rand];
        shuffled[rand] = value;
      }
    });
    return shuffled;
  };

  // Sort the object's values by a criterion produced by an iterator.
  _.sortBy = function(obj, iterator, context) {
    return _.pluck(_.map(obj, function(value, index, list) {
      return {
        value : value,
        criteria : iterator.call(context, value, index, list)
      };
    }).sort(function(left, right) {
      var a = left.criteria, b = right.criteria;
      return a < b ? -1 : a > b ? 1 : 0;
    }), 'value');
  };

  // Groups the object's values by a criterion. Pass either a string attribute
  // to group by, or a function that returns the criterion.
  _.groupBy = function(obj, val) {
    var result = {};
    var iterator = _.isFunction(val) ? val : function(obj) { return obj[val]; };
    each(obj, function(value, index) {
      var key = iterator(value, index);
      (result[key] || (result[key] = [])).push(value);
    });
    return result;
  };

  // Use a comparator function to figure out at what index an object should
  // be inserted so as to maintain order. Uses binary search.
  _.sortedIndex = function(array, obj, iterator) {
    iterator || (iterator = _.identity);
    var low = 0, high = array.length;
    while (low < high) {
      var mid = (low + high) >> 1;
      iterator(array[mid]) < iterator(obj) ? low = mid + 1 : high = mid;
    }
    return low;
  };

  // Safely convert anything iterable into a real, live array.
  _.toArray = function(iterable) {
    if (!iterable)                return [];
    if (iterable.toArray)         return iterable.toArray();
    if (_.isArray(iterable))      return slice.call(iterable);
    if (_.isArguments(iterable))  return slice.call(iterable);
    return _.values(iterable);
  };

  // Return the number of elements in an object.
  _.size = function(obj) {
    return _.toArray(obj).length;
  };

  // Array Functions
  // ---------------

  // Get the first element of an array. Passing **n** will return the first N
  // values in the array. Aliased as `head`. The **guard** check allows it to work
  // with `_.map`.
  _.first = _.head = function(array, n, guard) {
    return (n != null) && !guard ? slice.call(array, 0, n) : array[0];
  };

  // Returns everything but the last entry of the array. Especcialy useful on
  // the arguments object. Passing **n** will return all the values in
  // the array, excluding the last N. The **guard** check allows it to work with
  // `_.map`.
  _.initial = function(array, n, guard) {
    return slice.call(array, 0, array.length - ((n == null) || guard ? 1 : n));
  };

  // Get the last element of an array. Passing **n** will return the last N
  // values in the array. The **guard** check allows it to work with `_.map`.
  _.last = function(array, n, guard) {
    if ((n != null) && !guard) {
      return slice.call(array, Math.max(array.length - n, 0));
    } else {
      return array[array.length - 1];
    }
  };

  // Returns everything but the first entry of the array. Aliased as `tail`.
  // Especially useful on the arguments object. Passing an **index** will return
  // the rest of the values in the array from that index onward. The **guard**
  // check allows it to work with `_.map`.
  _.rest = _.tail = function(array, index, guard) {
    return slice.call(array, (index == null) || guard ? 1 : index);
  };

  // Trim out all falsy values from an array.
  _.compact = function(array) {
    return _.filter(array, function(value){ return !!value; });
  };

  // Return a completely flattened version of an array.
  _.flatten = function(array, shallow) {
    return _.reduce(array, function(memo, value) {
      if (_.isArray(value)) return memo.concat(shallow ? value : _.flatten(value));
      memo[memo.length] = value;
      return memo;
    }, []);
  };

  // Return a version of the array that does not contain the specified value(s).
  _.without = function(array) {
    return _.difference(array, slice.call(arguments, 1));
  };

  // Produce a duplicate-free version of the array. If the array has already
  // been sorted, you have the option of using a faster algorithm.
  // Aliased as `unique`.
  _.uniq = _.unique = function(array, isSorted, iterator) {
    var initial = iterator ? _.map(array, iterator) : array;
    var result = [];
    _.reduce(initial, function(memo, el, i) {
      if (0 == i || (isSorted === true ? _.last(memo) != el : !_.include(memo, el))) {
        memo[memo.length] = el;
        result[result.length] = array[i];
      }
      return memo;
    }, []);
    return result;
  };

  // Produce an array that contains the union: each distinct element from all of
  // the passed-in arrays.
  _.union = function() {
    return _.uniq(_.flatten(arguments, true));
  };

  // Produce an array that contains every item shared between all the
  // passed-in arrays. (Aliased as "intersect" for back-compat.)
  _.intersection = _.intersect = function(array) {
    var rest = slice.call(arguments, 1);
    return _.filter(_.uniq(array), function(item) {
      return _.every(rest, function(other) {
        return _.indexOf(other, item) >= 0;
      });
    });
  };

  // Take the difference between one array and a number of other arrays.
  // Only the elements present in just the first array will remain.
  _.difference = function(array) {
    var rest = _.flatten(slice.call(arguments, 1));
    return _.filter(array, function(value){ return !_.include(rest, value); });
  };

  // Zip together multiple lists into a single array -- elements that share
  // an index go together.
  _.zip = function() {
    var args = slice.call(arguments);
    var length = _.max(_.pluck(args, 'length'));
    var results = new Array(length);
    for (var i = 0; i < length; i++) results[i] = _.pluck(args, "" + i);
    return results;
  };

  // If the browser doesn't supply us with indexOf (I'm looking at you, **MSIE**),
  // we need this function. Return the position of the first occurrence of an
  // item in an array, or -1 if the item is not included in the array.
  // Delegates to **ECMAScript 5**'s native `indexOf` if available.
  // If the array is large and already in sort order, pass `true`
  // for **isSorted** to use binary search.
  _.indexOf = function(array, item, isSorted) {
    if (array == null) return -1;
    var i, l;
    if (isSorted) {
      i = _.sortedIndex(array, item);
      return array[i] === item ? i : -1;
    }
    if (nativeIndexOf && array.indexOf === nativeIndexOf) return array.indexOf(item);
    for (i = 0, l = array.length; i < l; i++) if (i in array && array[i] === item) return i;
    return -1;
  };

  // Delegates to **ECMAScript 5**'s native `lastIndexOf` if available.
  _.lastIndexOf = function(array, item) {
    if (array == null) return -1;
    if (nativeLastIndexOf && array.lastIndexOf === nativeLastIndexOf) return array.lastIndexOf(item);
    var i = array.length;
    while (i--) if (i in array && array[i] === item) return i;
    return -1;
  };

  // Generate an integer Array containing an arithmetic progression. A port of
  // the native Python `range()` function. See
  // [the Python documentation](http://docs.python.org/library/functions.html#range).
  _.range = function(start, stop, step) {
    if (arguments.length <= 1) {
      stop = start || 0;
      start = 0;
    }
    step = arguments[2] || 1;

    var len = Math.max(Math.ceil((stop - start) / step), 0);
    var idx = 0;
    var range = new Array(len);

    while(idx < len) {
      range[idx++] = start;
      start += step;
    }

    return range;
  };

  // Function (ahem) Functions
  // ------------------

  // Reusable constructor function for prototype setting.
  var ctor = function(){};

  // Create a function bound to a given object (assigning `this`, and arguments,
  // optionally). Binding with arguments is also known as `curry`.
  // Delegates to **ECMAScript 5**'s native `Function.bind` if available.
  // We check for `func.bind` first, to fail fast when `func` is undefined.
  _.bind = function bind(func, context) {
    if(!func) {
      return;
    }
    var bound, args;
    if (func.bind === nativeBind && nativeBind) return nativeBind.apply(func, slice.call(arguments, 1));
    if (!_.isFunction(func)) throw new TypeError;
    args = slice.call(arguments, 2);
    return bound = function() {
      if (!(this instanceof bound)) return func.apply(context, args.concat(slice.call(arguments)));
      ctor.prototype = func.prototype;
      var self = new ctor;
      var result = func.apply(self, args.concat(slice.call(arguments)));
      if (Object(result) === result) return result;
      return self;
    };
  };

  // Bind all of an object's methods to that object. Useful for ensuring that
  // all callbacks defined on an object belong to it.
  _.bindAll = function(obj) {
    var funcs = slice.call(arguments, 1);
    if (funcs.length == 0) funcs = _.functions(obj);
    each(funcs, function(f) { obj[f] = _.bind(obj[f], obj); });
    return obj;
  };

  // Memoize an expensive function by storing its results.
  _.memoize = function(func, hasher) {
    var memo = {};
    hasher || (hasher = _.identity);
    return function() {
      var key = hasher.apply(this, arguments);
      return _.has(memo, key) ? memo[key] : (memo[key] = func.apply(this, arguments));
    };
  };

  // Delays a function for the given number of milliseconds, and then calls
  // it with the arguments supplied.
  _.delay = function(func, wait) {
    var args = slice.call(arguments, 2);
    return setTimeout(function(){ return func.apply(func, args); }, wait);
  };

  // Defers a function, scheduling it to run after the current call stack has
  // cleared.
  _.defer = function(func) {
    return _.delay.apply(_, [func, 1].concat(slice.call(arguments, 1)));
  };

  // Returns a function, that, when invoked, will only be triggered at most once
  // during a given window of time.
  _.throttle = function(func, wait, options) {
    var timeout, context, args, result;
    var previous = 0;
    if (!options) options = {};

    var later = function() {
      previous = options.leading === false ? 0 : _.now();
      timeout = null;
      result = func.apply(context, args);
      if (!timeout) context = args = null;
    };

    var throttled = function() {
      var now = _.now();
      if (!previous && options.leading === false) previous = now;
      var remaining = wait - (now - previous);
      context = this;
      args = arguments;
      if (remaining <= 0 || remaining > wait) {
        if (timeout) {
          clearTimeout(timeout);
          timeout = null;
        }
        previous = now;
        result = func.apply(context, args);
        if (!timeout) context = args = null;
      } else if (!timeout && options.trailing !== false) {
        timeout = setTimeout(later, remaining);
      }
      return result;
    };

    throttled.cancel = function() {
      clearTimeout(timeout);
      previous = 0;
      timeout = context = args = null;
    };

    return throttled;
  };

  // Returns a function, that, as long as it continues to be invoked, will not
  // be triggered. The function will be called after it stops being called for
  // N milliseconds.
  _.debounce = function(func, wait) {
    var timeout;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        func.apply(context, args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  };

  // Returns a function that will be executed at most one time, no matter how
  // often you call it. Useful for lazy initialization.
  _.once = function(func) {
    var ran = false, memo;
    return function() {
      if (ran) return memo;
      ran = true;
      return memo = func.apply(this, arguments);
    };
  };

  // Returns the first function passed as an argument to the second,
  // allowing you to adjust arguments, run code before and after, and
  // conditionally execute the original function.
  _.wrap = function(func, wrapper) {
    return function() {
      var args = [func].concat(slice.call(arguments, 0));
      return wrapper.apply(this, args);
    };
  };

  // Returns a function that is the composition of a list of functions, each
  // consuming the return value of the function that follows.
  _.compose = function() {
    var funcs = arguments;
    return function() {
      var args = arguments;
      for (var i = funcs.length - 1; i >= 0; i--) {
        args = [funcs[i].apply(this, args)];
      }
      return args[0];
    };
  };

  // Returns a function that will only be executed after being called N times.
  _.after = function(times, func) {
    if (times <= 0) return func();
    return function() {
      if (--times < 1) { return func.apply(this, arguments); }
    };
  };

  // Object Functions
  // ----------------

  // Retrieve the names of an object's properties.
  // Delegates to **ECMAScript 5**'s native `Object.keys`
  _.keys = nativeKeys || function(obj) {
    if (obj !== Object(obj)) throw new TypeError('Invalid object');
    var keys = [];
    for (var key in obj) if (_.has(obj, key)) keys[keys.length] = key;
    return keys;
  };

  // Retrieve the values of an object's properties.
  _.values = function(obj) {
    return _.map(obj, _.identity);
  };

  // Return a sorted list of the function names available on the object.
  // Aliased as `methods`
  _.functions = _.methods = function(obj) {
    var names = [];
    for (var key in obj) {
      if (_.isFunction(obj[key])) names.push(key);
    }
    return names.sort();
  };

  // Extend a given object with all the properties in passed-in object(s).
  _.extend = function(obj) {
    each(slice.call(arguments, 1), function(source) {
      for (var prop in source) {
        obj[prop] = source[prop];
      }
    });
    return obj;
  };

  // Fill in a given object with default properties.
  _.defaults = function(obj) {
    each(slice.call(arguments, 1), function(source) {
      for (var prop in source) {
        if (obj[prop] == null) obj[prop] = source[prop];
      }
    });
    return obj;
  };

  // Create a (shallow-cloned) duplicate of an object.
  _.clone = function(obj) {
    if (!_.isObject(obj)) return obj;
    return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
  };

  // Invokes interceptor with the obj, and then returns obj.
  // The primary purpose of this method is to "tap into" a method chain, in
  // order to perform operations on intermediate results within the chain.
  _.tap = function(obj, interceptor) {
    interceptor(obj);
    return obj;
  };

  // Internal recursive comparison function.
  function eq(a, b, stack) {
    // Identical objects are equal. `0 === -0`, but they aren't identical.
    // See the Harmony `egal` proposal: http://wiki.ecmascript.org/doku.php?id=harmony:egal.
    if (a === b) return a !== 0 || 1 / a == 1 / b;
    // A strict comparison is necessary because `null == undefined`.
    if (a == null || b == null) return a === b;
    // Unwrap any wrapped objects.
    if (a._chain) a = a._wrapped;
    if (b._chain) b = b._wrapped;
    // Invoke a custom `isEqual` method if one is provided.
    if (a.isEqual && _.isFunction(a.isEqual)) return a.isEqual(b);
    if (b.isEqual && _.isFunction(b.isEqual)) return b.isEqual(a);
    // Compare `[[Class]]` names.
    var className = toString.call(a);
    if (className != toString.call(b)) return false;
    switch (className) {
      // Strings, numbers, dates, and booleans are compared by value.
      case '[object String]':
        // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
        // equivalent to `new String("5")`.
        return a == String(b);
      case '[object Number]':
        // `NaN`s are equivalent, but non-reflexive. An `egal` comparison is performed for
        // other numeric values.
        return a != +a ? b != +b : (a == 0 ? 1 / a == 1 / b : a == +b);
      case '[object Date]':
      case '[object Boolean]':
        // Coerce dates and booleans to numeric primitive values. Dates are compared by their
        // millisecond representations. Note that invalid dates with millisecond representations
        // of `NaN` are not equivalent.
        return +a == +b;
      // RegExps are compared by their source patterns and flags.
      case '[object RegExp]':
        return a.source == b.source &&
               a.global == b.global &&
               a.multiline == b.multiline &&
               a.ignoreCase == b.ignoreCase;
    }
    if (typeof a != 'object' || typeof b != 'object') return false;
    // Assume equality for cyclic structures. The algorithm for detecting cyclic
    // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.
    var length = stack.length;
    while (length--) {
      // Linear search. Performance is inversely proportional to the number of
      // unique nested structures.
      if (stack[length] == a) return true;
    }
    // Add the first object to the stack of traversed objects.
    stack.push(a);
    var size = 0, result = true;
    // Recursively compare objects and arrays.
    if (className == '[object Array]') {
      // Compare array lengths to determine if a deep comparison is necessary.
      size = a.length;
      result = size == b.length;
      if (result) {
        // Deep compare the contents, ignoring non-numeric properties.
        while (size--) {
          // Ensure commutative equality for sparse arrays.
          if (!(result = size in a == size in b && eq(a[size], b[size], stack))) break;
        }
      }
    } else {
      // Objects with different constructors are not equivalent.
      if ('constructor' in a != 'constructor' in b || a.constructor != b.constructor) return false;
      // Deep compare objects.
      for (var key in a) {
        if (_.has(a, key)) {
          // Count the expected number of properties.
          size++;
          // Deep compare each member.
          if (!(result = _.has(b, key) && eq(a[key], b[key], stack))) break;
        }
      }
      // Ensure that both objects contain the same number of properties.
      if (result) {
        for (key in b) {
          if (_.has(b, key) && !(size--)) break;
        }
        result = !size;
      }
    }
    // Remove the first object from the stack of traversed objects.
    stack.pop();
    return result;
  }

  // Perform a deep comparison to check if two objects are equal.
  _.isEqual = function(a, b) {
    return eq(a, b, []);
  };

  // Is a given array, string, or object empty?
  // An "empty" object has no enumerable own-properties.
  _.isEmpty = function(obj) {
    if (_.isArray(obj) || _.isString(obj)) return obj.length === 0;
    for (var key in obj) if (_.has(obj, key)) return false;
    return true;
  };

  // Is a given value a DOM element?
  _.isElement = function(obj) {
    return !!(obj && obj.nodeType == 1);
  };

  // Is a given value an array?
  // Delegates to ECMA5's native Array.isArray
  _.isArray = nativeIsArray || function(obj) {
    return toString.call(obj) == '[object Array]';
  };

  // Is a given variable an object?
  _.isObject = function(obj) {
    return obj === Object(obj);
  };

  // Is a given variable an arguments object?
  _.isArguments = function(obj) {
    return toString.call(obj) == '[object Arguments]';
  };
  if (!_.isArguments(arguments)) {
    _.isArguments = function(obj) {
      return !!(obj && _.has(obj, 'callee'));
    };
  }

  // Is a given value a function?
  _.isFunction = function(obj) {
    return toString.call(obj) == '[object Function]';
  };

  // Is a given value a string?
  _.isString = function(obj) {
    return toString.call(obj) == '[object String]';
  };

  // Is a given value a number?
  _.isNumber = function(obj) {
    return toString.call(obj) == '[object Number]';
  };

  // Is a given object a finite number?
  _.isFinite = function(obj) {
    return _.isNumber(obj) && isFinite(obj);
  };

  // Is the given value `NaN`?
  _.isNaN = function(obj) {
    // `NaN` is the only value for which `===` is not reflexive.
    return obj !== obj;
  };

  // Is a given value a boolean?
  _.isBoolean = function(obj) {
    return obj === true || obj === false || toString.call(obj) == '[object Boolean]';
  };

  // Is a given value a date?
  _.isDate = function(obj) {
    return toString.call(obj) == '[object Date]';
  };

  // Is the given value a regular expression?
  _.isRegExp = function(obj) {
    return toString.call(obj) == '[object RegExp]';
  };

  // Is a given value equal to null?
  _.isNull = function(obj) {
    return obj === null;
  };

  // Is a given variable undefined?
  _.isUndefined = function(obj) {
    return obj === void 0;
  };

  // Has own property?
  _.has = function(obj, key) {
    return hasOwnProperty.call(obj, key);
  };

  // Utility Functions
  // -----------------

  // Run Underscore.js in *noConflict* mode, returning the `_` variable to its
  // previous owner. Returns a reference to the Underscore object.
  _.noConflict = function() {
    root._ = previousUnderscore;
    return this;
  };

  // Keep the identity function around for default iterators.
  _.identity = function(value) {
    return value;
  };

  // Run a function **n** times.
  _.times = function (n, iterator, context) {
    for (var i = 0; i < n; i++) iterator.call(context, i);
  };

  // Escape a string for HTML interpolation.
  _.escape = function(string) {
    return (''+string).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;').replace(/\//g,'&#x2F;');
  };

  // Add your own custom functions to the Underscore object, ensuring that
  // they're correctly added to the OOP wrapper as well.
  _.mixin = function(obj) {
    each(_.functions(obj), function(name){
      addToWrapper(name, _[name] = obj[name]);
    });
  };

  // Generate a unique integer id (unique within the entire client session).
  // Useful for temporary DOM ids.
  var idCounter = 0;
  _.uniqueId = function(prefix) {
    var id = idCounter++;
    return prefix ? prefix + id : id;
  };

  // By default, Underscore uses ERB-style template delimiters, change the
  // following template settings to use alternative delimiters.
  _.templateSettings = {
    evaluate    : /<%([\s\S]+?)%>/g,
    interpolate : /<%=([\s\S]+?)%>/g,
    escape      : /<%-([\s\S]+?)%>/g
  };

  // When customizing `templateSettings`, if you don't want to define an
  // interpolation, evaluation or escaping regex, we need one that is
  // guaranteed not to match.
  var noMatch = /.^/;

  // Within an interpolation, evaluation, or escaping, remove HTML escaping
  // that had been previously added.
  var unescape = function(code) {
    return code.replace(/\\\\/g, '\\').replace(/\\'/g, "'");
  };

  // JavaScript micro-templating, similar to John Resig's implementation.
  // Underscore templating handles arbitrary delimiters, preserves whitespace,
  // and correctly escapes quotes within interpolated code.
  _.template = function(str, data) {
    var c  = _.templateSettings;
    var tmpl = 'var __p=[],print=function(){__p.push.apply(__p,arguments);};' +
      'with(obj||{}){__p.push(\'' +
      str.replace(/\\/g, '\\\\')
         .replace(/'/g, "\\'")
         .replace(c.escape || noMatch, function(match, code) {
           return "',_.escape(" + unescape(code) + "),'";
         })
         .replace(c.interpolate || noMatch, function(match, code) {
           return "'," + unescape(code) + ",'";
         })
         .replace(c.evaluate || noMatch, function(match, code) {
           return "');" + unescape(code).replace(/[\r\n\t]/g, ' ') + ";__p.push('";
         })
         .replace(/\r/g, '\\r')
         .replace(/\n/g, '\\n')
         .replace(/\t/g, '\\t')
         + "');}return __p.join('');";
    var func = new Function('obj', '_', tmpl);
    if (data) return func(data, _);
    return function(data) {
      return func.call(this, data, _);
    };
  };

  // Add a "chain" function, which will delegate to the wrapper.
  _.chain = function(obj) {
    return _(obj).chain();
  };

  // The OOP Wrapper
  // ---------------

  // If Underscore is called as a function, it returns a wrapped object that
  // can be used OO-style. This wrapper holds altered versions of all the
  // underscore functions. Wrapped objects may be chained.
  var wrapper = function(obj) { this._wrapped = obj; };

  // Expose `wrapper.prototype` as `_.prototype`
  _.prototype = wrapper.prototype;

  // Helper function to continue chaining intermediate results.
  var result = function(obj, chain) {
    return chain ? _(obj).chain() : obj;
  };

  // A method to easily add functions to the OOP wrapper.
  var addToWrapper = function(name, func) {
    wrapper.prototype[name] = function() {
      var args = slice.call(arguments);
      unshift.call(args, this._wrapped);
      return result(func.apply(_, args), this._chain);
    };
  };

  // Add all of the Underscore functions to the wrapper object.
  _.mixin(_);

  // Add all mutator Array functions to the wrapper.
  each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
    var method = ArrayProto[name];
    wrapper.prototype[name] = function() {
      var wrapped = this._wrapped;
      method.apply(wrapped, arguments);
      var length = wrapped.length;
      if ((name == 'shift' || name == 'splice') && length === 0) delete wrapped[0];
      return result(wrapped, this._chain);
    };
  });

  // Add all accessor Array functions to the wrapper.
  each(['concat', 'join', 'slice'], function(name) {
    var method = ArrayProto[name];
    wrapper.prototype[name] = function() {
      return result(method.apply(this._wrapped, arguments), this._chain);
    };
  });

  // Start chaining a wrapped Underscore object.
  wrapper.prototype.chain = function() {
    this._chain = true;
    return this;
  };

  // Extracts the result from a wrapped and chained object.
  wrapper.prototype.value = function() {
    return this._wrapped;
  };

}).call(this);
/*
 * jQote2 - client-side Javascript templating engine
 * Copyright (C) 2010, aefxx
 * http://aefxx.com/
 *
 * Dual licensed under the WTFPL v2 or MIT (X11) licenses
 * WTFPL v2 Copyright (C) 2004, Sam Hocevar
 *
 * Date: Thu, Oct 21st, 2010
 * Version: 0.9.7
 */
(function($) {
    var JQOTE2_TMPL_UNDEF_ERROR = 'UndefinedTemplateError',
        JQOTE2_TMPL_COMP_ERROR  = 'TemplateCompilationError',
        JQOTE2_TMPL_EXEC_ERROR  = 'TemplateExecutionError';

    var ARR  = '[object Array]',
        STR  = '[object String]',
        FUNC = '[object Function]';

    var n = 1, tag = '%',
        qreg = /^[^<]*(<[\w\W]+>)[^>]*$/,
        type_of = Object.prototype.toString;

    function raise(error, ext) {
        throw ($.extend(error, ext), error);
    }

    function dotted_ns(fn) {
        var ns = [];

        if ( type_of.call(fn) !== ARR ) return false;

        for ( var i=0,l=fn.length; i < l; i++ )
            ns[i] = fn[i].jqote_id;

        return ns.length ?
            ns.sort().join('.').replace(/(\b\d+\b)\.(?:\1(\.|$))+/g, '$1$2') : false;
    }

    function lambda(tmpl, t) {
        var f, fn = [], t = t || tag,
            type = type_of.call(tmpl);

        if ( type === FUNC )
            return tmpl.jqote_id ? [tmpl] : false;

        if ( type !== ARR )
            return [$.jqotec(tmpl, t)];

        if ( type === ARR )
            for ( var i=0,l=tmpl.length; i < l; i++ )
                if ( f = lambda(tmpl[i], t) ) fn.push(f[0]);

        return fn.length ? fn : false;
    }

    $.fn.extend({
        jqote: function(data, t) {
            var data = type_of.call(data) === ARR ? data : [data],
                dom = '';

            this.each(function(i) {
                var fn = $.jqotec(this, t);

                for ( var j=0; j < data.length; j++ )
                    dom += fn.call(data[j], i, j, data, fn);
            });

            return dom;
        }
    });

    $.each({app: 'append', pre: 'prepend', sub: 'html'}, function(name, method) {
        $.fn['jqote'+name] = function(elem, data, t) {
            var ns, regexp, str = $.jqote(elem, data, t),
                $$ = !qreg.test(str) ?
                    function(str) {return $(document.createTextNode(str));} : $;

            if ( !!(ns = dotted_ns(lambda(elem))) )
                regexp = new RegExp('(^|\\.)'+ns.split('.').join('\\.(.*)?')+'(\\.|$)');

            return this.each(function() {
                var dom = $$(str);

                $(this)[method](dom);

                ( dom[0].nodeType === 3 ?
                    $(this) : dom ).trigger('jqote.'+name, [dom, regexp]);
            });
        };
    });

    $.extend({
        jqote: function(elem, data, t) {
            var str = '', t = t || tag,
                fn = lambda(elem);

            if ( fn === false )
                raise(new Error('Empty or undefined template passed to $.jqote ' + elem), {type: JQOTE2_TMPL_UNDEF_ERROR});

            data = type_of.call(data) !== ARR ?
                [data] : data;

            for ( var i=0,l=fn.length; i < l; i++ )
                for ( var j=0; j < data.length; j++ )
                    str += fn[i].call(data[j], i, j, data, fn[i]);

            return str;
        },

        jqotec: function(template, t) {
            var cache, elem, tmpl, t = t || tag,
                type = type_of.call(template);

            if ( type === STR && qreg.test(template) ) {
                elem = tmpl = template;

                if ( cache = $.jqotecache[template] ) return cache;
            } else {
                elem = type === STR || template.nodeType ?
                    $(template) : template instanceof jQuery ?
                        template : null;

                if ( !elem[0] || !(tmpl = elem[0].innerHTML) && !(tmpl = elem.text()) ) {
                    console.log("Error finding template " + template);
                    raise(new Error('Empty or undefined template passed to $.jqotec'), {type: JQOTE2_TMPL_UNDEF_ERROR});
                }

                if ( cache = $.jqotecache[$.data(elem[0], 'jqote_id')] ) return cache;
            }

            var str = '', index,
                arr = tmpl.replace(/\s*<!\[CDATA\[\s*|\s*\]\]>\s*|[\r\n\t]/g, '')
                    .split('<'+t).join(t+'>\x1b')
                        .split(t+'>');

            for ( var m=0,l=arr.length; m < l; m++ )
                str += arr[m].charAt(0) !== '\x1b' ?
                    "out+='" + arr[m].replace(/(\\|["'])/g, '\\$1') + "'" : (arr[m].charAt(1) === '=' ?
                        ';out+=(' + arr[m].substr(2) + ');' : (arr[m].charAt(1) === '!' ?
                            ';out+=$.jqotenc((' + arr[m].substr(2) + '));' : ';' + arr[m].substr(1)));

            str = 'try{' +
                ('var out="";'+str+';return out;')
                    .split("out+='';").join('')
                        .split('var out="";out+=').join('var out=') +
                '}catch(e){e.type="'+JQOTE2_TMPL_EXEC_ERROR+'";e.args=arguments;e.template=arguments.callee.toString();throw e;}';

            try {
                var fn = new Function('i, j, data, fn', str);
            } catch ( e ) { raise(e, {type: JQOTE2_TMPL_COMP_ERROR}); }

            index = elem instanceof jQuery ?
                $.data(elem[0], 'jqote_id', n) : elem;

            return $.jqotecache[index] = (fn.jqote_id = n++, fn);
        },

        jqotefn: function(elem) {
            var type = type_of.call(elem),
                index = type === STR && qreg.test(elem) ?
                    elem : $.data($(elem)[0], 'jqote_id');

            return $.jqotecache[index] || false;
        },

        jqotetag: function(str) {
            if ( type_of.call(str) === STR ) tag = str;
        },

        jqotenc: function(str) {
            return str.toString()
                    .replace(/&(?!\w+;)/g, '&#38;')
                        .split('<').join('&#60;').split('>').join('&#62;')
                            .split('"').join('&#34;').split("'").join('&#39;');
        },

        jqotecache: {}
    });

    $.event.special.jqote = {
        add: function(obj) {
            var ns, handler = obj.handler,
                data = !obj.data ?
                    [] : type_of.call(obj.data) !== ARR ?
                        [obj.data] : obj.data;

            if ( !obj.namespace ) obj.namespace = 'app.pre.sub';
            if ( !data.length || !(ns = dotted_ns(lambda(data))) ) return;

            obj.handler = function(event, dom, regexp) {
                return !regexp || regexp.test(ns) ?
                    handler.apply(this, [event, dom]) : null;
            };
        }
    };
})(jQuery);

$(function() { $.jqotetag( '$' ); });
// Generated by CoffeeScript 1.7.1
(function() {
  var autoLink,
    __slice = [].slice;

  autoLink = function() {
    var k, linkAttributes, option, options, pattern, v;
    options = 1 <= arguments.length ? __slice.call(arguments, 0) : [];

    pattern = /(^|[\s\n]|<br\/?>)((?:https?|ftp):\/\/[\-A-Z0-9+\u0026\u2019@#\/%?=()~_|!:,.;]*[\-A-Z0-9+\u0026@#\/%=~()_|])/gi;
    if (!(options.length > 0)) {
      return this.replace(pattern, "$1<a href='$2'>$2</a>");
    }
    option = options[0];
    linkAttributes = ((function() {
      var _results;
      _results = [];
      for (k in option) {
        v = option[k];
        if (k !== 'callback') {
          _results.push(" " + k + "='" + v + "'");
        }
      }
      return _results;
    })()).join('');
    return this.replace(pattern, function(match, space, url) {
      var link;
      link = (typeof option.callback === "function" ? option.callback(url) : void 0) || ("<a href='" + url + "'" + linkAttributes + ">" + url + "</a>");
      return "" + space + link;
    });
  };

  String.prototype['autoLink'] = autoLink;

}).call(this);
//IMPORTANT: This has been modified from the original version to allow the 'accept' property on all elements, the 'name' and 'required' property on spans, and the 'data-i18n'/'data-i18n-vars' property on all elements.

{var CSS_PROP_BIT_QUANTITY=1,CSS_PROP_BIT_HASH_VALUE=2,CSS_PROP_BIT_NEGATIVE_QUANTITY=4,CSS_PROP_BIT_QSTRING_CONTENT=8,CSS_PROP_BIT_QSTRING_URL=16,CSS_PROP_BIT_HISTORY_INSENSITIVE=32,CSS_PROP_BIT_Z_INDEX=64,CSS_PROP_BIT_ALLOWED_IN_LINK=128,cssSchema=(function(){var
s=['rgb(?:\\(\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)\\s*,\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)\\s*,\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)|a\\(\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)\\s*,\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)\\s*,\\s*(?:\\d+|0|\\d+(?:\\.\\d+)?%)\\s*,\\s*(?:\\d+|0(?:\\.\\d+)?|\\.\\d+|1(?:\\.0+)?|0|\\d+(?:\\.\\d+)?%)) *\\)'],c=[/^ *$/i,RegExp('^ *\\s*'+s[0]+' *$','i'),RegExp('^ *(?:\\s*'+s[0]+'|(?:\\s*'+s[0]+')?)+ *$','i')],L=[['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgray','darkgreen','darkkhaki','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue','darkslategray','darkturquoise','darkviolet','deeppink','deepskyblue','dimgray','dodgerblue','firebrick','floralwhite','forestgreen','fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray','green','greenyellow','honeydew','hotpink','indianred','indigo','ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgreen','lightgrey','lightpink','lightsalmon','lightseagreen','lightskyblue','lightslategray','lightsteelblue','lightyellow','lime','limegreen','linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite','navy','oldlace','olive','olivedrab','orange','orangered','orchid','palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum','powderblue','purple','red','rosybrown','royalblue','saddlebrown','salmon','sandybrown','seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','snow','springgreen','steelblue','tan','teal','thistle','tomato','turquoise','violet','wheat','white','whitesmoke','yellow','yellowgreen'],['all-scroll','col-resize','crosshair','default','e-resize','hand','help','move','n-resize','ne-resize','no-drop','not-allowed','nw-resize','pointer','progress','row-resize','s-resize','se-resize','sw-resize','text','vertical-text','w-resize','wait'],['-moz-inline-box','-moz-inline-stack','block','inline','inline-block','inline-table','list-item','run-in','table','table-caption','table-cell','table-column','table-column-group','table-footer-group','table-header-group','table-row','table-row-group'],['armenian','circle','decimal','decimal-leading-zero','disc','georgian','lower-alpha','lower-greek','lower-latin','lower-roman','square','upper-alpha','upper-latin','upper-roman'],['100','200','300','400','500','600','700','800','900','bold','bolder','lighter'],['condensed','expanded','extra-condensed','extra-expanded','narrower','semi-condensed','semi-expanded','ultra-condensed','ultra-expanded','wider'],['behind','center-left','center-right','far-left','far-right','left-side','leftwards','right-side','rightwards'],['large','larger','small','smaller','x-large','x-small','xx-large','xx-small'],['-moz-pre-wrap','-o-pre-wrap','-pre-wrap','nowrap','pre','pre-line','pre-wrap'],['dashed','dotted','double','groove','outset','ridge','solid'],['baseline','middle','sub','super','text-bottom','text-top'],['caption','icon','menu','message-box','small-caption','status-bar'],['fast','faster','slow','slower','x-fast','x-slow'],['above','below','higher','level','lower'],['border-box','contain','content-box','cover','padding-box'],['cursive','fantasy','monospace','sans-serif','serif'],['loud','silent','soft','x-loud','x-soft'],['no-repeat','repeat-x','repeat-y','round','space'],['blink','line-through','overline','underline'],['high','low','x-high','x-low'],['absolute','relative','static'],['capitalize','lowercase','uppercase'],['child','female','male'],['bidi-override','embed'],['bottom','top'],['clip','ellipsis'],['continuous','digits'],['hide','show'],['inside','outside'],['italic','oblique'],['left','right'],['ltr','rtl'],['no-content','no-display'],['suppress','unrestricted'],['thick','thin'],[','],['/'],['always'],['auto'],['avoid'],['both'],['break-word'],['center'],['code'],['collapse'],['fixed'],['hidden'],['inherit'],['inset'],['invert'],['justify'],['local'],['medium'],['mix'],['none'],['normal'],['once'],['repeat'],['scroll'],['separate'],['small-caps'],['spell-out'],['transparent'],['visible']];return{'-moz-border-radius':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[36]]},'-moz-border-radius-bottomleft':{'cssExtra':c[0],'cssPropBits':5},'-moz-border-radius-bottomright':{'cssExtra':c[0],'cssPropBits':5},'-moz-border-radius-topleft':{'cssExtra':c[0],'cssPropBits':5},'-moz-border-radius-topright':{'cssExtra':c[0],'cssPropBits':5},'-moz-box-shadow':{'cssExtra':c[2],'cssAlternates':['boxShadow'],'cssPropBits':7,'cssLitGroup':[L[0],L[35],L[48],L[54]]},'-moz-opacity':{'cssPropBits':1,'cssLitGroup':[L[47]]},'-moz-outline':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[49],L[52],L[54]]},'-moz-outline-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[49]]},'-moz-outline-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'-moz-outline-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'-o-text-overflow':{'cssPropBits':0,'cssLitGroup':[L[25]]},'-webkit-border-bottom-left-radius':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-bottom-right-radius':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-radius':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[36]]},'-webkit-border-radius-bottom-left':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-radius-bottom-right':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-radius-top-left':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-radius-top-right':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-top-left-radius':{'cssExtra':c[0],'cssPropBits':5},'-webkit-border-top-right-radius':{'cssExtra':c[0],'cssPropBits':5},'-webkit-box-shadow':{'cssExtra':c[2],'cssAlternates':['boxShadow'],'cssPropBits':7,'cssLitGroup':[L[0],L[35],L[48],L[54]]},'azimuth':{'cssPropBits':5,'cssLitGroup':[L[6],L[30],L[42],L[47]]},'background':{'cssExtra':RegExp('^ *(?:\\s*'+s[0]+'){0,2} *$','i'),'cssPropBits':23,'cssLitGroup':[L[0],L[14],L[17],L[24],L[30],L[35],L[36],L[38],L[42],L[45],L[47],L[51],L[54],L[57],L[58],L[62]]},'background-size':{'cssExtra':RegExp('^ *(?:\\s*'+s[0]+'){0,2} *$','i'),'cssPropBits':23,'cssLitGroup':[L[0],L[14],L[17],L[24],L[30],L[35],L[36],L[38],L[42],L[45],L[47],L[51],L[54],L[57],L[58],L[62]]},'background-attachment':{'cssExtra':c[0],'cssPropBits':0,'cssLitGroup':[L[35],L[45],L[51],L[58]]},'background-color':{'cssExtra':c[1],'cssPropBits':130,'cssLitGroup':[L[0],L[47],L[62]]},'background-image':{'cssExtra':RegExp('.*','i'),'cssPropBits':16,'cssLitGroup':[L[35],L[54]]},'background-position':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[24],L[30],L[35],L[42]]},'background-repeat':{'cssExtra':c[0],'cssPropBits':0,'cssLitGroup':[L[17],L[35],L[57]]},'border':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[52],L[54],L[62]]},'border-bottom':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[52],L[54],L[62]]},'border-bottom-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[62]]},'border-bottom-left-radius':{'cssExtra':c[0],'cssPropBits':5},'border-bottom-right-radius':{'cssExtra':c[0],'cssPropBits':5},'border-bottom-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'border-bottom-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'border-collapse':{'cssPropBits':0,'cssLitGroup':[L[44],L[47],L[59]]},'border-color':{'cssExtra':RegExp('^ *(?:\\s*'+s[0]+'){1,4} *$','i'),'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[62]]},'border-left':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[52],L[54],L[62]]},'border-left-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[62]]},'border-left-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'border-left-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'border-radius':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[36]]},'border-right':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[52],L[54],L[62]]},'border-right-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[62]]},'border-right-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'border-right-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'border-spacing':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[47]]},'border-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'border-top':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[52],L[54],L[62]]},'border-top-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[62]]},'border-top-left-radius':{'cssExtra':c[0],'cssPropBits':5},'border-top-right-radius':{'cssExtra':c[0],'cssPropBits':5},'border-top-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'border-top-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'border-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'bottom':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'box-shadow':{'cssExtra':c[2],'cssPropBits':7,'cssLitGroup':[L[0],L[35],L[48],L[54]]},'caption-side':{'cssPropBits':0,'cssLitGroup':[L[24],L[47]]},'clear':{'cssPropBits':0,'cssLitGroup':[L[30],L[40],L[47],L[54]]},'clip':{'cssExtra':/^ *\s*rect\(\s*(?:0|[+\-]?\d+(?:\.\d+)?(?:[cem]m|ex|in|p[ctx])|auto)\s*,\s*(?:0|[+\-]?\d+(?:\.\d+)?(?:[cem]m|ex|in|p[ctx])|auto)\s*,\s*(?:0|[+\-]?\d+(?:\.\d+)?(?:[cem]m|ex|in|p[ctx])|auto)\s*,\s*(?:0|[+\-]?\d+(?:\.\d+)?(?:[cem]m|ex|in|p[ctx])|auto) *\) *$/i,'cssPropBits':0,'cssLitGroup':[L[38],L[47]]},'color':{'cssExtra':c[1],'cssPropBits':130,'cssLitGroup':[L[0],L[47]]},'content':{'cssPropBits':8,'cssLitGroup':[L[54],L[55]]},'counter-increment':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[47],L[54]]},'counter-reset':{'cssExtra':c[0],'cssPropBits':5,'cssLitGroup':[L[47],L[54]]},'cue':{'cssPropBits':16,'cssLitGroup':[L[47],L[54]]},'cue-after':{'cssPropBits':16,'cssLitGroup':[L[47],L[54]]},'cue-before':{'cssPropBits':16,'cssLitGroup':[L[47],L[54]]},'cursor':{'cssExtra':c[0],'cssPropBits':144,'cssLitGroup':[L[1],L[35],L[38],L[47]]},'direction':{'cssPropBits':0,'cssLitGroup':[L[31],L[47]]},'display':{'cssPropBits':32,'cssLitGroup':[L[2],L[47],L[54]]},'elevation':{'cssPropBits':5,'cssLitGroup':[L[13],L[47]]},'empty-cells':{'cssPropBits':0,'cssLitGroup':[L[27],L[47]]},'filter':{'cssExtra':/^ *(?:\s*alpha\(\s*opacity\s*=\s*(?:0|\d+(?:\.\d+)?%|[+\-]?\d+(?:\.\d+)?) *\))+ *$/i,'cssPropBits':32},'float':{'cssAlternates':['cssFloat','styleFloat'],'cssPropBits':32,'cssLitGroup':[L[30],L[47],L[54]]},'font':{'cssExtra':c[0],'cssPropBits':9,'cssLitGroup':[L[4],L[7],L[11],L[15],L[29],L[35],L[36],L[47],L[52],L[55],L[60]]},'font-family':{'cssExtra':c[0],'cssPropBits':8,'cssLitGroup':[L[15],L[35],L[47]]},'font-size':{'cssPropBits':1,'cssLitGroup':[L[7],L[47],L[52]]},'font-stretch':{'cssPropBits':0,'cssLitGroup':[L[5],L[55]]},'font-style':{'cssPropBits':0,'cssLitGroup':[L[29],L[47],L[55]]},'font-variant':{'cssPropBits':0,'cssLitGroup':[L[47],L[55],L[60]]},'font-weight':{'cssPropBits':0,'cssLitGroup':[L[4],L[47],L[55]]},'height':{'cssPropBits':37,'cssLitGroup':[L[38],L[47]]},'left':{'cssPropBits':37,'cssLitGroup':[L[38],L[47]]},'letter-spacing':{'cssPropBits':5,'cssLitGroup':[L[47],L[55]]},'line-height':{'cssPropBits':1,'cssLitGroup':[L[47],L[55]]},'list-style':{'cssPropBits':16,'cssLitGroup':[L[3],L[28],L[47],L[54]]},'list-style-image':{'cssPropBits':16,'cssLitGroup':[L[47],L[54]]},'list-style-position':{'cssPropBits':0,'cssLitGroup':[L[28],L[47]]},'list-style-type':{'cssPropBits':0,'cssLitGroup':[L[3],L[47],L[54]]},'margin':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'margin-bottom':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'margin-left':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'margin-right':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'margin-top':{'cssPropBits':5,'cssLitGroup':[L[38],L[47]]},'max-height':{'cssPropBits':1,'cssLitGroup':[L[38],L[47],L[54]]},'max-width':{'cssPropBits':1,'cssLitGroup':[L[38],L[47],L[54]]},'min-height':{'cssPropBits':1,'cssLitGroup':[L[38],L[47]]},'min-width':{'cssPropBits':1,'cssLitGroup':[L[38],L[47]]},'opacity':{'cssPropBits':33,'cssLitGroup':[L[47]]},'outline':{'cssExtra':c[1],'cssPropBits':7,'cssLitGroup':[L[0],L[9],L[34],L[46],L[47],L[48],L[49],L[52],L[54]]},'outline-color':{'cssExtra':c[1],'cssPropBits':2,'cssLitGroup':[L[0],L[47],L[49]]},'outline-style':{'cssPropBits':0,'cssLitGroup':[L[9],L[46],L[47],L[48],L[54]]},'outline-width':{'cssPropBits':5,'cssLitGroup':[L[34],L[47],L[52]]},'overflow':{'cssPropBits':32,'cssLitGroup':[L[38],L[46],L[47],L[58],L[63]]},'overflow-x':{'cssPropBits':0,'cssLitGroup':[L[32],L[38],L[46],L[58],L[63]]},'overflow-y':{'cssPropBits':0,'cssLitGroup':[L[32],L[38],L[46],L[58],L[63]]},'padding':{'cssPropBits':1,'cssLitGroup':[L[47]]},'padding-bottom':{'cssPropBits':33,'cssLitGroup':[L[47]]},'padding-left':{'cssPropBits':33,'cssLitGroup':[L[47]]},'padding-right':{'cssPropBits':33,'cssLitGroup':[L[47]]},'padding-top':{'cssPropBits':33,'cssLitGroup':[L[47]]},'page-break-after':{'cssPropBits':0,'cssLitGroup':[L[30],L[37],L[38],L[39],L[47]]},'page-break-before':{'cssPropBits':0,'cssLitGroup':[L[30],L[37],L[38],L[39],L[47]]},'page-break-inside':{'cssPropBits':0,'cssLitGroup':[L[38],L[39],L[47]]},'pause':{'cssPropBits':5,'cssLitGroup':[L[47]]},'pause-after':{'cssPropBits':5,'cssLitGroup':[L[47]]},'pause-before':{'cssPropBits':5,'cssLitGroup':[L[47]]},'pitch':{'cssPropBits':5,'cssLitGroup':[L[19],L[47],L[52]]},'pitch-range':{'cssPropBits':5,'cssLitGroup':[L[47]]},'play-during':{'cssExtra':c[0],'cssPropBits':16,'cssLitGroup':[L[38],L[47],L[53],L[54],L[57]]},'position':{'cssPropBits':32,'cssLitGroup':[L[20],L[47]]},'quotes':{'cssExtra':c[0],'cssPropBits':8,'cssLitGroup':[L[47],L[54]]},'richness':{'cssPropBits':5,'cssLitGroup':[L[47]]},'right':{'cssPropBits':37,'cssLitGroup':[L[38],L[47]]},'speak':{'cssPropBits':0,'cssLitGroup':[L[47],L[54],L[55],L[61]]},'speak-header':{'cssPropBits':0,'cssLitGroup':[L[37],L[47],L[56]]},'speak-numeral':{'cssPropBits':0,'cssLitGroup':[L[26],L[47]]},'speak-punctuation':{'cssPropBits':0,'cssLitGroup':[L[43],L[47],L[54]]},'speech-rate':{'cssPropBits':5,'cssLitGroup':[L[12],L[47],L[52]]},'stress':{'cssPropBits':5,'cssLitGroup':[L[47]]},'table-layout':{'cssPropBits':0,'cssLitGroup':[L[38],L[45],L[47]]},'text-align':{'cssPropBits':0,'cssLitGroup':[L[30],L[42],L[47],L[50]]},'text-decoration':{'cssPropBits':0,'cssLitGroup':[L[18],L[47],L[54]]},'text-indent':{'cssPropBits':5,'cssLitGroup':[L[47]]},'text-overflow':{'cssPropBits':0,'cssLitGroup':[L[25]]},'text-shadow':{'cssExtra':c[2],'cssPropBits':7,'cssLitGroup':[L[0],L[35],L[48],L[54]]},'text-transform':{'cssPropBits':0,'cssLitGroup':[L[21],L[47],L[54]]},'text-wrap':{'cssPropBits':0,'cssLitGroup':[L[33],L[54],L[55]]},'top':{'cssPropBits':37,'cssLitGroup':[L[38],L[47]]},'unicode-bidi':{'cssPropBits':0,'cssLitGroup':[L[23],L[47],L[55]]},'vertical-align':{'cssPropBits':5,'cssLitGroup':[L[10],L[24],L[47]]},'visibility':{'cssPropBits':32,'cssLitGroup':[L[44],L[46],L[47],L[63]]},'voice-family':{'cssExtra':c[0],'cssPropBits':8,'cssLitGroup':[L[22],L[35],L[47]]},'volume':{'cssPropBits':1,'cssLitGroup':[L[16],L[47],L[52]]},'white-space':{'cssPropBits':0,'cssLitGroup':[L[8],L[47],L[55]]},'width':{'cssPropBits':33,'cssLitGroup':[L[38],L[47]]},'word-spacing':{'cssPropBits':5,'cssLitGroup':[L[47],L[55]]},'word-wrap':{'cssPropBits':0,'cssLitGroup':[L[41],L[55]]},'z-index':{'cssPropBits':69,'cssLitGroup':[L[38],L[47]]},'zoom':{'cssPropBits':1,'cssLitGroup':[L[55]]}}})(),URI,decodeCss,html,html4,html_sanitize,lexCss,parseCssDeclarations,parseCssStylesheet,sanitizeCssProperty,sanitizeCssSelectors,sanitizeStylesheet,sanitizeStylesheetWithExternals;typeof
window!=='undefined'&&(window['cssSchema']=cssSchema),(function(){var ATKEYWORD,BOM,CDC,CDO,CHAR,CMP_OPS,COMMENT,CSS_TOKEN,DASHMATCH,DIMENSION,ESCAPE,ESCAPE_TAIL,FUNCTION,HASH,IDENT,INCLUDES,NAME,NL,NMCHAR,NMSTART,NONASCII,NUM,NUMBER,NUMERIC_VALUE,PERCENTAGE,PREFIXMATCH,S,STRING,STRINGCHAR,SUBSTRINGMATCH,SUFFIXMATCH,SURROGATE_PAIR,UNICODE,UNICODE_RANGE,UNICODE_TAIL,URI,URLCHAR,W,WC,WORD_TERM,cssStrChars,cssUrlChars;function
decodeCssEscape(s){var i=parseInt(s.substring(1),16);return i>65535?(i-=65536,String.fromCharCode(55296+(i>>10),56320+(i&1023))):i==i?String.fromCharCode(i):s[1]<' '?'':s[1]}function
escapeCssString(s,replacer){return'\"'+s.replace(/[\u0000-\u001f\\\"\x3c\x3e]/g,replacer)+'\"'}function
escapeCssStrChar(ch){return cssStrChars[ch]||(cssStrChars[ch]='\\'+ch.charCodeAt(0).toString(16)+' ')}function
escapeCssUrlChar(ch){return cssUrlChars[ch]||(cssUrlChars[ch]=(ch<'\x10'?'%0':'%')+ch.charCodeAt(0).toString(16))}cssStrChars={'\\':'\\\\'},cssUrlChars={'\\':'%5c'},WC='[\\t\\n\\f ]',W=WC+'*',NL='[\\n\\f]',SURROGATE_PAIR='[\\ud800-\\udbff][\\udc00-\\udfff]',NONASCII='[\\u0080-\\ud7ff\\ue000-\\ufffd]|'+SURROGATE_PAIR,UNICODE_TAIL='[0-9a-fA-F]{1,6}'+WC+'?',UNICODE='\\\\'+UNICODE_TAIL,ESCAPE_TAIL='(?:'+UNICODE_TAIL+'|[\\u0020-\\u007e\\u0080-\\ud7ff\\ue000\\ufffd]|'+SURROGATE_PAIR+')',ESCAPE='\\\\'+ESCAPE_TAIL,URLCHAR='(?:[\\t\\x21\\x23-\\x26\\x28-\\x5b\\x5d-\\x7e]|'+NONASCII+'|'+ESCAPE+')',STRINGCHAR='[^\'\"\\n\\f\\\\]|\\\\[\\s\\S]',STRING='\"(?:\'|'+STRINGCHAR+')*\"'+'|\'(?:\"|'+STRINGCHAR+')*\'',NUM='[-+]?(?:[0-9]+(?:[.][0-9]+)?|[.][0-9]+)',NMSTART='(?:[a-zA-Z_]|'+NONASCII+'|'+ESCAPE+')',NMCHAR='(?:[a-zA-Z0-9_-]|'+NONASCII+'|'+ESCAPE+')',NAME=NMCHAR+'+',IDENT='-?'+NMSTART+NMCHAR+'*',ATKEYWORD='@'+IDENT,HASH='#'+NAME,NUMBER=NUM,WORD_TERM='(?:@?-?'+NMSTART+'|#)'+NMCHAR+'*',PERCENTAGE=NUM+'%',DIMENSION=NUM+IDENT,NUMERIC_VALUE=NUM+'(?:%|'+IDENT+')?',URI='url[(]'+W+'(?:'+STRING+'|'+URLCHAR+'*)'+W+'[)]',UNICODE_RANGE='U[+][0-9A-F?]{1,6}(?:-[0-9A-F]{1,6})?',CDO='\x3c!--',CDC='--\x3e',S=WC+'+',COMMENT='/(?:[*][^*]*[*]+(?:[^/][^*]*[*]+)*/|/[^\\n\\f]*)',FUNCTION='(?!url[(])'+IDENT+'[(]',INCLUDES='~=',DASHMATCH='[|]=',PREFIXMATCH='[^]=',SUFFIXMATCH='[$]=',SUBSTRINGMATCH='[*]=',CMP_OPS='[~|^$*]=',CHAR='[^\"\'\\\\/]|/(?![/*])',BOM='\\uFEFF',CSS_TOKEN=new
RegExp(([BOM,UNICODE_RANGE,URI,FUNCTION,WORD_TERM,STRING,NUMERIC_VALUE,CDO,CDC,S,COMMENT,CMP_OPS,CHAR].join('|')),'gi'),decodeCss=function(css){return css.replace(new
RegExp(('\\\\(?:'+ESCAPE_TAIL+'|'+NL+')'),'g'),decodeCssEscape)},lexCss=function(cssText){var
cc,i,j,last,len,n,tok,tokens;cssText=''+cssText,tokens=cssText.replace(/\r\n?/g,'\n').match(CSS_TOKEN)||[],j=0,last=' ';for(i=0,n=tokens.length;i<n;++i)tok=decodeCss(tokens[i]),len=tok.length,cc=tok.charCodeAt(0),tok=cc=='\"'.charCodeAt(0)||cc=='\''.charCodeAt(0)?escapeCssString(tok.substring(1,len-1),escapeCssStrChar):cc=='/'.charCodeAt(0)&&len>1||tok=='\\'||tok==CDC||tok==CDO||tok=='\ufeff'||cc<=' '.charCodeAt(0)?' ':/url\(/i.test(tok)?'url('+escapeCssString(tok.replace(new
RegExp(('^url\\('+W+'[\"\']?|[\"\']?'+W+'\\)$'),'gi'),''),escapeCssUrlChar)+')':tok,(last!=tok||tok!=' ')&&(tokens[j++]=last=tok);return tokens.length=j,tokens}})(),typeof
window!=='undefined'&&(window['lexCss']=lexCss,window['decodeCss']=decodeCss),URI=(function(){var
EXTRA_PARENT_PATHS_RE,PARENT_DIRECTORY_HANDLER,PARENT_DIRECTORY_HANDLER_RE,URI_DISALLOWED_IN_PATH_,URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_,URI_RE_;function
parse(uriStr){var m=(''+uriStr).match(URI_RE_);return m?new URI((nullIfAbsent(m[1])),(nullIfAbsent(m[2])),(nullIfAbsent(m[3])),(nullIfAbsent(m[4])),(nullIfAbsent(m[5])),(nullIfAbsent(m[6])),(nullIfAbsent(m[7]))):null}function
create(scheme,credentials,domain,port,path,query,fragment){var uri=new URI((encodeIfExists2(scheme,URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_)),(encodeIfExists2(credentials,URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_)),(encodeIfExists(domain)),(port>0?port.toString():null),(encodeIfExists2(path,URI_DISALLOWED_IN_PATH_)),null,(encodeIfExists(fragment)));return query&&('string'===typeof
query?uri.setRawQuery(query.replace(/[^?\x26=0-9A-Za-z_\-~.%]/g,encodeOne)):uri.setAllParameters(query)),uri}function
encodeIfExists(unescapedPart){return'string'==typeof unescapedPart?encodeURIComponent(unescapedPart):null}function
encodeIfExists2(unescapedPart,extra){return'string'==typeof unescapedPart?encodeURI(unescapedPart).replace(extra,encodeOne):null}function
encodeOne(ch){var n=ch.charCodeAt(0);return'%'+'0123456789ABCDEF'.charAt(n>>4&15)+'0123456789ABCDEF'.charAt(n&15)}function
normPath(path){return path.replace(/(^|\/)\.(?:\/|$)/g,'$1').replace(/\/{2,}/g,'/')}PARENT_DIRECTORY_HANDLER=new
RegExp('(/|^)(?:[^./][^/]*|\\.{2,}(?:[^./][^/]*)|\\.{3,}[^/]*)/\\.\\.(?:/|$)'),PARENT_DIRECTORY_HANDLER_RE=new
RegExp(PARENT_DIRECTORY_HANDLER),EXTRA_PARENT_PATHS_RE=/^(?:\.\.\/)*(?:\.\.$)?/;function
collapse_dots(path){var p,q,r;if(path===null)return null;p=normPath(path),r=PARENT_DIRECTORY_HANDLER_RE;for(;(q=p.replace(r,'$1'))!=p;p=q);return p}function
resolve(baseUri,relativeUri){var absoluteUri=baseUri.clone(),overridden=relativeUri.hasScheme(),absRawPath,rawPath,simplifiedPath,slash;return overridden?absoluteUri.setRawScheme(relativeUri.getRawScheme()):(overridden=relativeUri.hasCredentials()),overridden?absoluteUri.setRawCredentials(relativeUri.getRawCredentials()):(overridden=relativeUri.hasDomain()),overridden?absoluteUri.setRawDomain(relativeUri.getRawDomain()):(overridden=relativeUri.hasPort()),rawPath=relativeUri.getRawPath(),simplifiedPath=collapse_dots(rawPath),overridden?(absoluteUri.setPort(relativeUri.getPort()),simplifiedPath=simplifiedPath&&simplifiedPath.replace(EXTRA_PARENT_PATHS_RE,'')):(overridden=!!rawPath,overridden?simplifiedPath.charCodeAt(0)!==47&&(absRawPath=collapse_dots(absoluteUri.getRawPath()||'').replace(EXTRA_PARENT_PATHS_RE,''),slash=absRawPath.lastIndexOf('/')+1,simplifiedPath=collapse_dots((slash?absRawPath.substring(0,slash):'')+collapse_dots(rawPath)).replace(EXTRA_PARENT_PATHS_RE,'')):(simplifiedPath=simplifiedPath&&simplifiedPath.replace(EXTRA_PARENT_PATHS_RE,''),simplifiedPath!==rawPath&&absoluteUri.setRawPath(simplifiedPath))),overridden?absoluteUri.setRawPath(simplifiedPath):(overridden=relativeUri.hasQuery()),overridden?absoluteUri.setRawQuery(relativeUri.getRawQuery()):(overridden=relativeUri.hasFragment()),overridden&&absoluteUri.setRawFragment(relativeUri.getRawFragment()),absoluteUri}function
URI(rawScheme,rawCredentials,rawDomain,port,rawPath,rawQuery,rawFragment){this.scheme_=rawScheme,this.credentials_=rawCredentials,this.domain_=rawDomain,this.port_=port,this.path_=rawPath,this.query_=rawQuery,this.fragment_=rawFragment,this.paramCache_=null}URI.prototype.toString=function(){var
out=[];return null!==this.scheme_&&out.push(this.scheme_,':'),null!==this.domain_&&(out.push('//'),null!==this.credentials_&&out.push(this.credentials_,'@'),out.push(this.domain_),null!==this.port_&&out.push(':',this.port_.toString())),null!==this.path_&&out.push(this.path_),null!==this.query_&&out.push('?',this.query_),null!==this.fragment_&&out.push('#',this.fragment_),out.join('')},URI.prototype.clone=function(){return new
URI(this.scheme_,this.credentials_,this.domain_,this.port_,this.path_,this.query_,this.fragment_)},URI.prototype.getScheme=function(){return this.scheme_&&decodeURIComponent(this.scheme_).toLowerCase()},URI.prototype.getRawScheme=function(){return this.scheme_},URI.prototype.setScheme=function(newScheme){return this.scheme_=encodeIfExists2(newScheme,URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_),this},URI.prototype.setRawScheme=function(newScheme){return this.scheme_=newScheme?newScheme:null,this},URI.prototype.hasScheme=function(){return null!==this.scheme_},URI.prototype.getCredentials=function(){return this.credentials_&&decodeURIComponent(this.credentials_)},URI.prototype.getRawCredentials=function(){return this.credentials_},URI.prototype.setCredentials=function(newCredentials){return this.credentials_=encodeIfExists2(newCredentials,URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_),this},URI.prototype.setRawCredentials=function(newCredentials){return this.credentials_=newCredentials?newCredentials:null,this},URI.prototype.hasCredentials=function(){return null!==this.credentials_},URI.prototype.getDomain=function(){return this.domain_&&decodeURIComponent(this.domain_)},URI.prototype.getRawDomain=function(){return this.domain_},URI.prototype.setDomain=function(newDomain){return this.setRawDomain(newDomain&&encodeURIComponent(newDomain))},URI.prototype.setRawDomain=function(newDomain){return this.domain_=newDomain?newDomain:null,this.setRawPath(this.path_)},URI.prototype.hasDomain=function(){return null!==this.domain_},URI.prototype.getPort=function(){return this.port_&&decodeURIComponent(this.port_)},URI.prototype.setPort=function(newPort){if(newPort){newPort=Number(newPort);if(newPort!==(newPort&65535))throw new
Error(('Bad port number '+newPort));this.port_=''+newPort}else this.port_=null;return this},URI.prototype.hasPort=function(){return null!==this.port_},URI.prototype.getPath=function(){return this.path_&&decodeURIComponent(this.path_)},URI.prototype.getRawPath=function(){return this.path_},URI.prototype.setPath=function(newPath){return this.setRawPath(encodeIfExists2(newPath,URI_DISALLOWED_IN_PATH_))},URI.prototype.setRawPath=function(newPath){return newPath?(newPath=String(newPath),this.path_=!this.domain_||/^\//.test(newPath)?newPath:'/'+newPath):(this.path_=null),this},URI.prototype.hasPath=function(){return null!==this.path_},URI.prototype.getQuery=function(){return this.query_&&decodeURIComponent(this.query_).replace(/\+/g,' ')},URI.prototype.getRawQuery=function(){return this.query_},URI.prototype.setQuery=function(newQuery){return this.paramCache_=null,this.query_=encodeIfExists(newQuery),this},URI.prototype.setRawQuery=function(newQuery){return this.paramCache_=null,this.query_=newQuery?newQuery:null,this},URI.prototype.hasQuery=function(){return null!==this.query_},URI.prototype.setAllParameters=function(params){var
i,j,k,newParams,queryBuf,separator,v;if(typeof params==='object'){if(!(params instanceof
Array)&&(params instanceof Object||Object.prototype.toString.call(params)!=='[object Array]')){newParams=[],i=-1;for(k
in params)v=params[k],'string'===typeof v&&(newParams[++i]=k,newParams[++i]=v);params=newParams}}this.paramCache_=null,queryBuf=[],separator='';for(j=0;j<params.length;)k=params[j++],v=params[j++],queryBuf.push(separator,encodeURIComponent(k.toString())),separator='\x26',v&&queryBuf.push('=',encodeURIComponent(v.toString()));return this.query_=queryBuf.join(''),this},URI.prototype.checkParameterCache_=function(){var
cgiParams,i,k,m,out,q;if(!this.paramCache_){q=this.query_;if(!q)this.paramCache_=[];else{cgiParams=q.split(/[\x26\?]/),out=[],k=-1;for(i=0;i<cgiParams.length;++i)m=cgiParams[i].match(/^([^=]*)(?:=(.*))?$/),out[++k]=decodeURIComponent(m[1]).replace(/\+/g,' '),out[++k]=decodeURIComponent(m[2]||'').replace(/\+/g,' ');this.paramCache_=out}}},URI.prototype.setParameterValues=function(key,values){var
i,k,newValueIndex,params,pc;typeof values==='string'&&(values=[values]),this.checkParameterCache_(),newValueIndex=0,pc=this.paramCache_,params=[];for(i=0,k=0;i<pc.length;i+=2)key===pc[i]?newValueIndex<values.length&&params.push(key,values[newValueIndex++]):params.push(pc[i],pc[i+1]);while(newValueIndex<values.length)params.push(key,values[newValueIndex++]);return this.setAllParameters(params),this},URI.prototype.removeParameter=function(key){return this.setParameterValues(key,[])},URI.prototype.getAllParameters=function(){return this.checkParameterCache_(),this.paramCache_.slice(0,this.paramCache_.length)},URI.prototype.getParameterValues=function(paramNameUnescaped){var
i,values;this.checkParameterCache_(),values=[];for(i=0;i<this.paramCache_.length;i+=2)paramNameUnescaped===this.paramCache_[i]&&values.push(this.paramCache_[i+1]);return values},URI.prototype.getParameterMap=function(paramNameUnescaped){var
i,key,paramMap,value;this.checkParameterCache_(),paramMap={};for(i=0;i<this.paramCache_.length;i+=2)key=this.paramCache_[i++],value=this.paramCache_[i++],key
in paramMap?paramMap[key].push(value):(paramMap[key]=[value]);return paramMap},URI.prototype.getParameterValue=function(paramNameUnescaped){var
i;this.checkParameterCache_();for(i=0;i<this.paramCache_.length;i+=2)if(paramNameUnescaped===this.paramCache_[i])return this.paramCache_[i+1];return null},URI.prototype.getFragment=function(){return this.fragment_&&decodeURIComponent(this.fragment_)},URI.prototype.getRawFragment=function(){return this.fragment_},URI.prototype.setFragment=function(newFragment){return this.fragment_=newFragment?encodeURIComponent(newFragment):null,this},URI.prototype.setRawFragment=function(newFragment){return this.fragment_=newFragment?newFragment:null,this},URI.prototype.hasFragment=function(){return null!==this.fragment_};function
nullIfAbsent(matchPart){return'string'==typeof matchPart&&matchPart.length>0?matchPart:null}return URI_RE_=new
RegExp('^(?:([^:/?#]+):)?(?://(?:([^/?#]*)@)?([^/?#:@]*)(?::([0-9]+))?)?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$'),URI_DISALLOWED_IN_SCHEME_OR_CREDENTIALS_=/[#\/\?@]/g,URI_DISALLOWED_IN_PATH_=/[\#\?]/g,URI.parse=parse,URI.create=create,URI.resolve=resolve,URI.collapse_dots=collapse_dots,URI.utils={'mimeTypeOf':function(uri){var
uriObj=parse(uri);return/\.html$/.test(uriObj.getPath())?'text/html':'application/javascript'},'resolve':function(base,uri){return base?resolve(parse(base),parse(uri)).toString():''+uri}},URI})(),typeof
window!=='undefined'&&(window['URI']=URI),sanitizeCssProperty=undefined,sanitizeCssSelectors=undefined,sanitizeStylesheet=undefined,sanitizeStylesheetWithExternals=undefined,(function(){var
NOEFFECT_URL='url(\"about:blank\")',NORM_URL_REGEXP=/[\n\f\r\"\'()*\x3c\x3e]/g,NORM_URL_REPLACEMENTS={'\n':'%0a','\f':'%0c','\r':'%0d','\"':'%22','\'':'%27','(':'%28',')':'%29','*':'%2a','\x3c':'%3c','\x3e':'%3e'},ALLOWED_URI_SCHEMES,URI_SCHEME_RE;function
normalizeUrl(s){return'string'===typeof s?'url(\"'+s.replace(NORM_URL_REGEXP,normalizeUrlChar)+'\")':NOEFFECT_URL}function
normalizeUrlChar(ch){return NORM_URL_REPLACEMENTS[ch]}URI_SCHEME_RE=new RegExp('^(?:([^:/?# ]+):)?'),ALLOWED_URI_SCHEMES=/^(?:https?|mailto)$/i;function
resolveUri(baseUri,uri){return baseUri?URI.utils.resolve(baseUri,uri):uri}function
safeUri(uri,prop,naiveUriRewriter){var parsed;return naiveUriRewriter?(parsed=(''+uri).match(URI_SCHEME_RE),parsed&&(!parsed[1]||ALLOWED_URI_SCHEMES.test(parsed[1]))?naiveUriRewriter(uri,prop):null):null}sanitizeCssProperty=(function(){var
ALLOWED_LITERAL;function unionArrays(arrs){var map={},arr,i,j;for(i=arrs.length;--i>=0;){arr=arrs[i];for(j=arr.length;--j>=0;)map[arr[j]]=ALLOWED_LITERAL}return map}function
normalizeFunctionCall(tokens,start){var parenDepth=1,end=start+1,n=tokens.length,token;while(end<n&&parenDepth)token=tokens[end++],parenDepth+=token==='('?1:token===')'?-1:0;return end}return ALLOWED_LITERAL={},function(property,propertySchema,tokens,opt_naiveUriRewriter,opt_baseUri){var
propBits=propertySchema.cssPropBits,qstringBits=propBits&(CSS_PROP_BIT_QSTRING_CONTENT|CSS_PROP_BIT_QSTRING_URL),lastQuoted=NaN,i=0,k=0,cc,cc1,cc2,end,isnum1,isnum2,litGroup,litMap,token;for(;i<tokens.length;++i)token=tokens[i].toLowerCase(),cc=token.charCodeAt(0),token=cc===' '.charCodeAt(0)?'':cc==='\"'.charCodeAt(0)?qstringBits===CSS_PROP_BIT_QSTRING_URL&&opt_naiveUriRewriter?normalizeUrl(safeUri(resolveUri(opt_baseUri,decodeCss(tokens[i].substring(1,token.length-1))),property,opt_naiveUriRewriter)):qstringBits===CSS_PROP_BIT_QSTRING_CONTENT?token:'':cc==='#'.charCodeAt(0)&&/^#(?:[0-9a-f]{3}){1,2}$/.test(token)?propBits&CSS_PROP_BIT_HASH_VALUE?token:'':'0'.charCodeAt(0)<=cc&&cc<='9'.charCodeAt(0)?propBits&CSS_PROP_BIT_QUANTITY?propBits&CSS_PROP_BIT_Z_INDEX?token.match(/^\d{1,7}$/)?token:'':token:'':(cc1=token.charCodeAt(1),cc2=token.charCodeAt(2),isnum1='0'.charCodeAt(0)<=cc1&&cc1<='9'.charCodeAt(0),isnum2='0'.charCodeAt(0)<=cc2&&cc2<='9'.charCodeAt(0),cc==='+'.charCodeAt(0)&&(isnum1||cc1==='.'.charCodeAt(0)&&isnum2))?propBits&CSS_PROP_BIT_QUANTITY?propBits&CSS_PROP_BIT_Z_INDEX?token.match(/^\+\d{1,7}$/)?token:'':(isnum1?'':'0')+token.substring(1):'':cc==='-'.charCodeAt(0)&&(isnum1||cc1==='.'.charCodeAt(0)&&isnum2)?propBits&CSS_PROP_BIT_NEGATIVE_QUANTITY?propBits&CSS_PROP_BIT_Z_INDEX?token.match(/^\-\d{1,7}$/)?token:'':(isnum1?'-':'-0')+token.substring(1):propBits&CSS_PROP_BIT_QUANTITY?'0':'':cc==='.'.charCodeAt(0)&&isnum1?propBits&CSS_PROP_BIT_QUANTITY?'0'+token:'':'url('===token.substring(0,4)?opt_naiveUriRewriter&&qstringBits&CSS_PROP_BIT_QSTRING_URL?normalizeUrl(safeUri(resolveUri(opt_baseUri,tokens[i].substring(5,token.length-2)),property,opt_naiveUriRewriter)):'':(token.charAt(token.length-1)==='('&&(end=normalizeFunctionCall(tokens,i),tokens.splice(i,end-i,token=tokens.slice(i,end).join(' '))),litGroup=propertySchema.cssLitGroup,litMap=litGroup?propertySchema.cssLitMap||(propertySchema.cssLitMap=unionArrays(litGroup)):ALLOWED_LITERAL,litMap[token]===ALLOWED_LITERAL||propertySchema.cssExtra&&propertySchema.cssExtra.test(token))?token:/^\w+$/.test(token)&&qstringBits===CSS_PROP_BIT_QSTRING_CONTENT?lastQuoted+1===k?(tokens[lastQuoted]=tokens[lastQuoted].substring(0,tokens[lastQuoted].length-1)+' '+token+'\"',token=''):(lastQuoted=k,'\"'+token+'\"'):'',token&&(tokens[k++]=token);k===1&&tokens[0]===NOEFFECT_URL&&(k=0),tokens.length=k}})(),sanitizeCssSelectors=function(selectors,suffix,tagPolicy){var
historySensitiveSelectors=[],historyInsensitiveSelectors=[],HISTORY_NON_SENSITIVE_PSEUDO_SELECTOR_WHITELIST=/^(active|after|before|first-child|first-letter|focus|hover)$/,HISTORY_SENSITIVE_PSEUDO_SELECTOR_WHITELIST=/^(link|visited)$/,k=0,inBrackets=0,i,n,start,tok;for(i=0;i<selectors.length;++i)tok=selectors[i],(tok=='('||tok=='['?(++inBrackets,true):tok==')'||tok==']'?(inBrackets&&--inBrackets,true):!(selectors[i]==' '&&(inBrackets||selectors[i-1]=='\x3e'||selectors[i+1]=='\x3e')))&&(selectors[k++]=selectors[i]);selectors.length=k,n=selectors.length,start=0;for(i=0;i<n;++i)selectors[i]===','&&(processSelector(start,i),start=i+1);processSelector(start,n);function
processSelector(start,end){var historySensitive=false,elSelector,i,isChild,lastOperator,out,safeSelector,tok;selectors[start]===' '&&++start,end-1!==start&&selectors[end]===' '&&--end,out=[],lastOperator=start,elSelector='';for(i=start;i<end;++i){tok=selectors[i],isChild=tok==='\x3e';if(isChild||tok===' '){elSelector=processElementSelector(lastOperator,i,false);if(!elSelector||isChild&&/^html/i.test(elSelector))return;lastOperator=i+1,out.push(elSelector,isChild?' \x3e ':' ')}}elSelector=processElementSelector(lastOperator,end,true);if(!elSelector)return;out.push(elSelector);function
processElementSelector(start,end,last){var element='',attr,attrs,atype,classId,decision,op,pseudoSelector,tok,value;start<end&&(tok=selectors[start],tok==='*'?(++start,element=tok):/^[a-zA-Z]/.test(tok)&&(decision=tagPolicy(tok.toLowerCase(),[]),decision&&('tagName'in
decision&&(tok=decision['tagName']),++start,element=tok))),classId='';while(start<end){tok=selectors[start];if(tok.charAt(0)==='#'){if(/^#_|__$|[^#0-9A-Za-z:_\-]/.test(tok))return null;classId+=tok+'-'+suffix}else
if(tok==='.')if(++start<end&&/^[0-9A-Za-z:_\-]+$/.test(tok=selectors[start])&&!/^_|__$/.test(tok))classId+='.'+tok;else
return null;else break;++start}attrs='';while(start<end&&selectors[start]==='['){++start,attr=selectors[start++],atype=html4.ATTRIBS[element+'::'+attr],atype!==+atype&&(atype=html4.ATTRIBS['*::'+attr]);if(atype!==+atype)return null;op='',value='',/^[~^$*|]?=$/.test(selectors[start])&&(op=selectors[start++],value=selectors[start++]);if(selectors[start++]!==']')return null;switch(atype){case
html4.atype['NONE']:case html4.atype['URI']:case html4.atype['URI_FRAGMENT']:case
html4.atype['ID']:case html4.atype['IDREF']:case html4.atype['IDREFS']:case html4.atype['GLOBAL_NAME']:case
html4.atype['LOCAL_NAME']:case html4.atype['CLASSES']:if(op&&atype!==html4.atype['NONE'])return null;attrs+='['+attr+op+value+']'}}pseudoSelector='';if(start<end&&selectors[start]===':'){tok=selectors[++start];if(HISTORY_SENSITIVE_PSEUDO_SELECTOR_WHITELIST.test(tok)){if(!/^[a*]?$/.test(element))return null;historySensitive=true,pseudoSelector=':'+tok,++start,element='a'}else
if(HISTORY_NON_SENSITIVE_PSEUDO_SELECTOR_WHITELIST.test(tok))historySensitive=false,pseudoSelector=':'+tok,++start}return start===end?(element+classId).replace(/[^ .*#\w-]/g,'\\$\x26')+attrs+pseudoSelector:null}safeSelector=out.join(''),safeSelector='.'+suffix+' '+safeSelector,(historySensitive?historySensitiveSelectors:historyInsensitiveSelectors).push(safeSelector)}return[historyInsensitiveSelectors,historySensitiveSelectors]},(function(){var
allowed={},cssMediaTypeWhitelist={'braille':allowed,'embossed':allowed,'handheld':allowed,'print':allowed,'projection':allowed,'screen':allowed,'speech':allowed,'tty':allowed,'tv':allowed};function
sanitizeHistorySensitive(blockOfProperties){var elide=false,i,n,token;for(i=0,n=blockOfProperties.length;i<n-1;++i)token=blockOfProperties[i],':'===blockOfProperties[i+1]&&(elide=!(cssSchema[token].cssPropBits&CSS_PROP_BIT_ALLOWED_IN_LINK)),elide&&(blockOfProperties[i]=''),';'===token&&(elide=false);return blockOfProperties.join('')}function
cssParseUri(candidate){var string1=/^\s*["]([^"]*)["]\s*$/,string2=/^\s*[']([^']*)[']\s*$/,url1=/^\s*url\s*[(]["]([^"]*)["][)]\s*$/,url2=/^\s*url\s*[(][']([^']*)['][)]\s*$/,url3=/^\s*url\s*[(]([^)]*)[)]\s*$/,match;return(match=string1.exec(candidate))?match[1]:(match=string2.exec(candidate))?match[1]:(match=url1.exec(candidate))?match[1]:(match=url2.exec(candidate))?match[1]:(match=url3.exec(candidate))?match[1]:null}function
sanitizeStylesheetInternal(baseUri,cssText,suffix,naiveUriRewriter,naiveUriFetcher,tagPolicy,continuation){var
safeCss=void 0,moreToCome=false,blockStack=[],elide=false;parseCssStylesheet(cssText,{'startStylesheet':function(){safeCss=[]},'endStylesheet':function(){},'startAtrule':function(atIdent,headerArray){var
cssUrl;elide?(atIdent=null):atIdent==='@media'?(headerArray=headerArray.filter(function(mediaType){return cssMediaTypeWhitelist[mediaType]==allowed}),headerArray.length?safeCss.push(atIdent,' ',headerArray.join(',')):(atIdent=null)):atIdent==='@import'&&headerArray.length>0&&('function'===typeof
continuation?(moreToCome=true,cssUrl=safeUri(resolveUri(baseUri,cssParseUri(headerArray[0])),function(result){var
sanitized=sanitizeStylesheetInternal(cssUrl,result.html,suffix,naiveUriRewriter,naiveUriFetcher,tagPolicy,continuation);continuation(sanitized.result,sanitized.moreToCome)},naiveUriFetcher)):window.console&&window.console.log('@import '+headerArray.join(' ')+' elided'),atIdent=null),elide=!atIdent,blockStack.push(atIdent)},'endAtrule':function(){var
atIdent=blockStack.pop();elide||safeCss.push(';'),checkElide()},'startBlock':function(){elide||safeCss.push('{')},'endBlock':function(){elide||(safeCss.push('}'),elide=true)},'startRuleset':function(selectorArray){var
historySensitiveSelectors=void 0,removeHistoryInsensitiveSelectors=false,historyInsensitiveSelectors,selector,selectors;elide||(selectors=sanitizeCssSelectors(selectorArray,suffix,tagPolicy),historyInsensitiveSelectors=selectors[0],historySensitiveSelectors=selectors[1],!historyInsensitiveSelectors.length&&!historySensitiveSelectors.length?(elide=true):(selector=historyInsensitiveSelectors.join(', '),selector||(selector='head \x3e html',removeHistoryInsensitiveSelectors=true),safeCss.push(selector,'{'))),blockStack.push(elide?null:{'historySensitiveSelectors':historySensitiveSelectors,'endOfSelectors':safeCss.length-1,'removeHistoryInsensitiveSelectors':removeHistoryInsensitiveSelectors})},'endRuleset':function(){var
rules=blockStack.pop(),propertiesEnd=safeCss.length,extraSelectors,propertyGroupTokens;elide||(safeCss.push('}'),rules&&(extraSelectors=rules.historySensitiveSelectors,extraSelectors.length&&(propertyGroupTokens=safeCss.slice(rules.endOfSelectors),safeCss.push(extraSelectors.join(', '),sanitizeHistorySensitive(propertyGroupTokens))))),rules&&rules.removeHistoryInsensitiveSelectors&&safeCss.splice(rules.endOfSelectors-1,propertiesEnd+1),checkElide()},'declaration':function(property,valueArray){var
schema;elide||(schema=cssSchema[property],schema&&(sanitizeCssProperty(property,schema,valueArray,naiveUriRewriter,baseUri),valueArray.length&&safeCss.push(property,':',valueArray.join(' '),';')))}});function
checkElide(){elide=blockStack.length!==0&&blockStack[blockStack.length-1]!==null&&blockStack[blockStack.length-1][0]!=='@'}return{'result':safeCss.join(''),'moreToCome':moreToCome}}sanitizeStylesheet=function(baseUri,cssText,suffix,naiveUriRewriter,tagPolicy){return sanitizeStylesheetInternal(baseUri,cssText,suffix,naiveUriRewriter,undefined,tagPolicy,undefined).result},sanitizeStylesheetWithExternals=function(baseUri,cssText,suffix,naiveUriRewriter,naiveUriFetcher,tagPolicy,continuation){return sanitizeStylesheetInternal(baseUri,cssText,suffix,naiveUriRewriter,naiveUriFetcher,tagPolicy,continuation)}})()})(),typeof
window!=='undefined'&&(window['sanitizeCssProperty']=sanitizeCssProperty,window['sanitizeCssSelectors']=sanitizeCssSelectors,window['sanitizeStylesheet']=sanitizeStylesheet);if('I'.toLowerCase()!=='i')throw'I/i problem';(function(){var
ident;parseCssStylesheet=function(cssText,handler){var toks=lexCss(cssText),i,n;handler.startStylesheet&&handler.startStylesheet();for(i=0,n=toks.length;i<n;)i=toks[i]===' '?i+1:statement(toks,i,n,handler);handler.endStylesheet&&handler.endStylesheet()};function
statement(toks,i,n,handler){var tok;return i<n?(tok=toks[i],tok.charAt(0)==='@'?atrule(toks,i,n,handler,true):ruleset(toks,i,n,handler)):i}function
atrule(toks,i,n,handler,blockok){var start=i++,e,s;while(i<n&&toks[i]!=='{'&&toks[i]!==';')++i;return i<n&&(blockok||toks[i]===';')&&(s=start+1,e=i,s<n&&toks[s]===' '&&++s,e>s&&toks[e-1]===' '&&--e,handler.startAtrule&&handler.startAtrule(toks[start].toLowerCase(),toks.slice(s,e)),i=toks[i]==='{'?block(toks,i,n,handler):i+1,handler.endAtrule&&handler.endAtrule()),i}function
block(toks,i,n,handler){var ch;++i,handler.startBlock&&handler.startBlock();while(i<n){ch=toks[i].charAt(0);if(ch=='}'){++i;break}ch===' '||ch===';'?(i=i+1):ch==='@'?(i=atrule(toks,i,n,handler,false)):ch==='{'?(i=block(toks,i,n,handler)):(i=ruleset(toks,i,n,handler))}return handler.endBlock&&handler.endBlock(),i}function
ruleset(toks,i,n,handler){var s=i,e=selector(toks,i,n,true),tok;if(e<0)return e=~e,i===e?e+1:e;i=e,e>s&&toks[e-1]===' '&&--e,tok=toks[i],++i;if(tok!=='{')return i;handler.startRuleset&&handler.startRuleset(toks.slice(s,e));while(i<n){tok=toks[i];if(tok==='}'){++i;break}tok===' '?(i=i+1):(i=declaration(toks,i,n,handler))}return handler.endRuleset&&handler.endRuleset(),i<n?i+1:i}function
selector(toks,i,n,allowSemi){var s=i,brackets=[],stackLast=-1,tok;for(;i<n;++i){tok=toks[i].charAt(0);if(tok==='['||tok==='(')brackets[++stackLast]=tok;else
if(tok===']'&&brackets[stackLast]==='['||tok===')'&&brackets[stackLast]==='(')--stackLast;else
if(tok==='{'||tok==='}'||tok===';'||tok==='@'||tok===':'&&!allowSemi)break}return stackLast>=0&&(i=~(i+1)),i}ident=/^-?[a-z]/i;function
declaration(toks,i,n,handler){var property=toks[i++],e,j,s,tok,value,valuelen;if(!ident.test(property))return i+1;i<n&&toks[i]===' '&&++i;if(i==n||toks[i]!==':'){while(i<n&&(tok=toks[i])!==';'&&tok!=='}')++i;return i}++i,i<n&&toks[i]===' '&&++i,s=i,e=selector(toks,i,n,false);if(e<0)e=~e;else{value=[],valuelen=0;for(j=s;j<e;++j)tok=toks[j],tok!==' '&&(value[valuelen++]=tok);if(e<n){do{tok=toks[e];if(tok===';'||tok==='}')break;valuelen=0}while(++e<n);tok===';'&&++e}valuelen&&handler.declaration&&handler.declaration(property.toLowerCase(),value)}return e}parseCssDeclarations=function(cssText,handler){var
toks=lexCss(cssText),i,n;for(i=0,n=toks.length;i<n;)i=toks[i]!==' '?declaration(toks,i,n,handler):i+1}})(),typeof
window!=='undefined'&&(window['parseCssStylesheet']=parseCssStylesheet,window['parseCssDeclarations']=parseCssDeclarations),html4={},html4.atype={'NONE':0,'URI':1,'URI_FRAGMENT':11,'SCRIPT':2,'STYLE':3,'HTML':12,'ID':4,'IDREF':5,'IDREFS':6,'GLOBAL_NAME':7,'LOCAL_NAME':8,'CLASSES':9,'FRAME_TARGET':10,'MEDIA_QUERY':13},html4['atype']=html4.atype,html4.ATTRIBS={'*::class':9,'*::dir':0,'*::draggable':0,'*::hidden':0,'*::id':4,'*::inert':0,'*::itemprop':0,'*::itemref':6,'*::itemscope':0,'*::lang':0,'*::onblur':2,'*::onchange':2,'*::onclick':2,'*::ondblclick':2,'*::onfocus':2,'*::onkeydown':2,'*::onkeypress':2,'*::onkeyup':2,'*::onload':2,'*::onmousedown':2,'*::onmousemove':2,'*::onmouseout':2,'*::onmouseover':2,'*::onmouseup':2,'*::onreset':2,'*::onscroll':2,'*::onselect':2,'*::onsubmit':2,'*::onunload':2,'*::spellcheck':0,'*::style':3,'*::title':0,'*::accept':0,'span::name':7,'span::required':0,'*::translate':0,'a::accesskey':0,'a::coords':0,'a::href':1,'a::hreflang':0,'a::name':7,'a::onblur':2,'a::onfocus':2,'a::shape':0,'a::tabindex':0,'a::target':10,'a::type':0,'area::accesskey':0,'area::alt':0,'area::coords':0,'area::href':1,'area::nohref':0,'area::onblur':2,'area::onfocus':2,'area::shape':0,'area::tabindex':0,'area::target':10,'audio::controls':0,'audio::loop':0,'audio::mediagroup':5,'audio::muted':0,'audio::preload':0,'bdo::dir':0,'blockquote::cite':1,'br::clear':0,'button::accesskey':0,'button::disabled':0,'button::name':8,'button::onblur':2,'button::onfocus':2,'button::tabindex':0,'button::type':0,'button::value':0,'canvas::height':0,'canvas::width':0,'caption::align':0,'col::align':0,'col::char':0,'col::charoff':0,'col::span':0,'col::valign':0,'col::width':0,'colgroup::align':0,'colgroup::char':0,'colgroup::charoff':0,'colgroup::span':0,'colgroup::valign':0,'colgroup::width':0,'command::checked':0,'command::command':5,'command::disabled':0,'command::icon':1,'command::label':0,'command::radiogroup':0,'command::type':0,'*::data-i18n':0,'*::data-i18n-list':0,'*::data-i18n-list-item':0,'*::data-i18n-list-item-num':0,'*::data-i18n-error':0,'*::data-i18n-dynamic':0,'*::data-i18n-vars':0,'*::data-i18n-placeholder':0,'*::data-i18n-title':0,'*::data-i18n-alt':0,'*::data-i18n-aria-label':0,'*::data-i18n-label':0,'data::value':0,'del::cite':1,'del::datetime':0,'details::open':0,'dir::compact':0,'div::align':0,'dl::compact':0,'fieldset::disabled':0,'font::color':0,'font::face':0,'font::size':0,'form::accept':0,'form::action':1,'form::autocomplete':0,'form::enctype':0,'form::method':0,'form::name':7,'form::novalidate':0,'form::onreset':2,'form::onsubmit':2,'form::target':10,'h1::align':0,'h2::align':0,'h3::align':0,'h4::align':0,'h5::align':0,'h6::align':0,'hr::align':0,'hr::noshade':0,'hr::size':0,'hr::width':0,'iframe::align':0,'iframe::frameborder':0,'iframe::height':0,'iframe::marginheight':0,'iframe::marginwidth':0,'iframe::width':0,'img::align':0,'img::alt':0,'img::border':0,'img::height':0,'img::hspace':0,'img::ismap':0,'img::name':7,'img::src':1,'img::usemap':11,'img::vspace':0,'img::width':0,'input::accept':0,'input::accesskey':0,'input::align':0,'input::alt':0,'input::autocomplete':0,'input::checked':0,'input::disabled':0,'input::inputmode':0,'input::ismap':0,'input::list':5,'input::max':0,'input::maxlength':0,'input::min':0,'input::multiple':0,'input::name':8,'input::onblur':2,'input::onchange':2,'input::onfocus':2,'input::onselect':2,'input::placeholder':0,'input::readonly':0,'input::required':0,'input::size':0,'input::src':1,'input::step':0,'input::tabindex':0,'input::type':0,'input::usemap':11,'input::value':0,'ins::cite':1,'ins::datetime':0,'label::accesskey':0,'label::for':5,'label::onblur':2,'label::onfocus':2,'legend::accesskey':0,'legend::align':0,'li::type':0,'li::value':0,'map::name':7,'menu::compact':0,'menu::label':0,'menu::type':0,'meter::high':0,'meter::low':0,'meter::max':0,'meter::min':0,'meter::value':0,'ol::compact':0,'ol::reversed':0,'ol::start':0,'ol::type':0,'optgroup::disabled':0,'optgroup::label':0,'option::disabled':0,'option::label':0,'option::selected':0,'option::value':0,'output::for':6,'output::name':8,'p::align':0,'pre::width':0,'progress::max':0,'progress::min':0,'progress::value':0,'q::cite':1,'select::autocomplete':0,'select::disabled':0,'select::multiple':0,'select::name':8,'select::onblur':2,'select::onchange':2,'select::onfocus':2,'select::required':0,'select::size':0,'select::tabindex':0,'source::type':0,'table::align':0,'table::bgcolor':0,'table::border':0,'table::cellpadding':0,'table::cellspacing':0,'table::frame':0,'table::rules':0,'table::summary':0,'table::width':0,'tbody::align':0,'tbody::char':0,'tbody::charoff':0,'tbody::valign':0,'td::abbr':0,'td::align':0,'td::axis':0,'td::bgcolor':0,'td::char':0,'td::charoff':0,'td::colspan':0,'td::headers':6,'td::height':0,'td::nowrap':0,'td::rowspan':0,'td::scope':0,'td::valign':0,'td::width':0,'textarea::accesskey':0,'textarea::autocomplete':0,'textarea::cols':0,'textarea::disabled':0,'textarea::inputmode':0,'textarea::name':8,'textarea::onblur':2,'textarea::onchange':2,'textarea::onfocus':2,'textarea::onselect':2,'textarea::placeholder':0,'textarea::readonly':0,'textarea::required':0,'textarea::rows':0,'textarea::tabindex':0,'textarea::wrap':0,'tfoot::align':0,'tfoot::char':0,'tfoot::charoff':0,'tfoot::valign':0,'th::abbr':0,'th::align':0,'th::axis':0,'th::bgcolor':0,'th::char':0,'th::charoff':0,'th::colspan':0,'th::headers':6,'th::height':0,'th::nowrap':0,'th::rowspan':0,'th::scope':0,'th::valign':0,'th::width':0,'thead::align':0,'thead::char':0,'thead::charoff':0,'thead::valign':0,'tr::align':0,'tr::bgcolor':0,'tr::char':0,'tr::charoff':0,'tr::valign':0,'track::default':0,'track::kind':0,'track::label':0,'track::srclang':0,'ul::compact':0,'ul::type':0,'video::controls':0,'video::height':0,'video::loop':0,'video::mediagroup':5,'video::muted':0,'video::poster':1,'video::preload':0,'video::width':0},html4['ATTRIBS']=html4.ATTRIBS,html4.eflags={'OPTIONAL_ENDTAG':1,'EMPTY':2,'CDATA':4,'RCDATA':8,'UNSAFE':16,'FOLDABLE':32,'SCRIPT':64,'STYLE':128,'VIRTUALIZED':256},html4['eflags']=html4.eflags,html4.ELEMENTS={'a':0,'abbr':0,'acronym':0,'address':0,'applet':272,'area':2,'article':0,'aside':0,'audio':0,'b':0,'base':274,'basefont':274,'bdi':0,'bdo':0,'big':0,'blockquote':0,'body':305,'br':2,'button':0,'canvas':0,'caption':0,'center':0,'cite':0,'code':0,'col':2,'colgroup':1,'command':2,'data':0,'datalist':0,'dd':1,'del':0,'details':0,'dfn':0,'dialog':272,'dir':0,'div':0,'dl':0,'dt':1,'em':0,'fieldset':0,'figcaption':0,'figure':0,'font':0,'footer':0,'form':0,'frame':274,'frameset':272,'h1':0,'h2':0,'h3':0,'h4':0,'h5':0,'h6':0,'head':305,'header':0,'hgroup':0,'hr':2,'html':305,'i':0,'iframe':4,'img':2,'input':2,'ins':0,'isindex':274,'kbd':0,'keygen':274,'label':0,'legend':0,'li':1,'link':274,'map':0,'mark':0,'menu':0,'meta':274,'meter':0,'nav':0,'nobr':0,'noembed':276,'noframes':276,'noscript':276,'object':272,'ol':0,'optgroup':0,'option':1,'output':0,'p':1,'param':274,'pre':0,'progress':0,'q':0,'s':0,'samp':0,'script':84,'section':0,'select':0,'small':0,'source':2,'span':0,'strike':0,'strong':0,'style':148,'sub':0,'summary':0,'sup':0,'table':0,'tbody':1,'td':1,'textarea':8,'tfoot':1,'th':1,'thead':1,'time':0,'title':280,'tr':1,'track':2,'tt':0,'u':0,'ul':0,'var':0,'video':0,'wbr':2},html4['ELEMENTS']=html4.ELEMENTS,html4.ELEMENT_DOM_INTERFACES={'a':'HTMLAnchorElement','abbr':'HTMLElement','acronym':'HTMLElement','address':'HTMLElement','applet':'HTMLAppletElement','area':'HTMLAreaElement','article':'HTMLElement','aside':'HTMLElement','audio':'HTMLAudioElement','b':'HTMLElement','base':'HTMLBaseElement','basefont':'HTMLBaseFontElement','bdi':'HTMLElement','bdo':'HTMLElement','big':'HTMLElement','blockquote':'HTMLQuoteElement','body':'HTMLBodyElement','br':'HTMLBRElement','button':'HTMLButtonElement','canvas':'HTMLCanvasElement','caption':'HTMLTableCaptionElement','center':'HTMLElement','cite':'HTMLElement','code':'HTMLElement','col':'HTMLTableColElement','colgroup':'HTMLTableColElement','command':'HTMLCommandElement','data':'HTMLElement','datalist':'HTMLDataListElement','dd':'HTMLElement','del':'HTMLModElement','details':'HTMLDetailsElement','dfn':'HTMLElement','dialog':'HTMLDialogElement','dir':'HTMLDirectoryElement','div':'HTMLDivElement','dl':'HTMLDListElement','dt':'HTMLElement','em':'HTMLElement','fieldset':'HTMLFieldSetElement','figcaption':'HTMLElement','figure':'HTMLElement','font':'HTMLFontElement','footer':'HTMLElement','form':'HTMLFormElement','frame':'HTMLFrameElement','frameset':'HTMLFrameSetElement','h1':'HTMLHeadingElement','h2':'HTMLHeadingElement','h3':'HTMLHeadingElement','h4':'HTMLHeadingElement','h5':'HTMLHeadingElement','h6':'HTMLHeadingElement','head':'HTMLHeadElement','header':'HTMLElement','hgroup':'HTMLElement','hr':'HTMLHRElement','html':'HTMLHtmlElement','i':'HTMLElement','iframe':'HTMLIFrameElement','img':'HTMLImageElement','input':'HTMLInputElement','ins':'HTMLModElement','isindex':'HTMLUnknownElement','kbd':'HTMLElement','keygen':'HTMLKeygenElement','label':'HTMLLabelElement','legend':'HTMLLegendElement','li':'HTMLLIElement','link':'HTMLLinkElement','map':'HTMLMapElement','mark':'HTMLElement','menu':'HTMLMenuElement','meta':'HTMLMetaElement','meter':'HTMLMeterElement','nav':'HTMLElement','nobr':'HTMLElement','noembed':'HTMLElement','noframes':'HTMLElement','noscript':'HTMLElement','object':'HTMLObjectElement','ol':'HTMLOListElement','optgroup':'HTMLOptGroupElement','option':'HTMLOptionElement','output':'HTMLOutputElement','p':'HTMLParagraphElement','param':'HTMLParamElement','pre':'HTMLPreElement','progress':'HTMLProgressElement','q':'HTMLQuoteElement','s':'HTMLElement','samp':'HTMLElement','script':'HTMLScriptElement','section':'HTMLElement','select':'HTMLSelectElement','small':'HTMLElement','source':'HTMLSourceElement','span':'HTMLSpanElement','strike':'HTMLElement','strong':'HTMLElement','style':'HTMLStyleElement','sub':'HTMLElement','summary':'HTMLElement','sup':'HTMLElement','table':'HTMLTableElement','tbody':'HTMLTableSectionElement','td':'HTMLTableDataCellElement','textarea':'HTMLTextAreaElement','tfoot':'HTMLTableSectionElement','th':'HTMLTableHeaderCellElement','thead':'HTMLTableSectionElement','time':'HTMLTimeElement','title':'HTMLTitleElement','tr':'HTMLTableRowElement','track':'HTMLTrackElement','tt':'HTMLElement','u':'HTMLElement','ul':'HTMLUListElement','var':'HTMLElement','video':'HTMLVideoElement','wbr':'HTMLElement'},html4['ELEMENT_DOM_INTERFACES']=html4.ELEMENT_DOM_INTERFACES,html4.ueffects={'NOT_LOADED':0,'SAME_DOCUMENT':1,'NEW_DOCUMENT':2},html4['ueffects']=html4.ueffects,html4.URIEFFECTS={'a::href':2,'area::href':2,'blockquote::cite':0,'command::icon':1,'del::cite':0,'form::action':2,'img::src':1,'input::src':1,'ins::cite':0,'q::cite':0,'video::poster':1},html4['URIEFFECTS']=html4.URIEFFECTS,html4.ltypes={'UNSANDBOXED':2,'SANDBOXED':1,'DATA':0},html4['ltypes']=html4.ltypes,html4.LOADERTYPES={'a::href':2,'area::href':2,'blockquote::cite':2,'command::icon':1,'del::cite':2,'form::action':2,'img::src':1,'input::src':1,'ins::cite':2,'q::cite':2,'video::poster':1},html4['LOADERTYPES']=html4.LOADERTYPES,typeof
window!=='undefined'&&(window['html4']=html4);if('I'.toLowerCase()!=='i')throw'I/i problem';html=(function(html4){var
ALLOWED_URI_SCHEMES,ATTR_RE,EFLAGS_TEXT,ENTITIES,ENTITY_RE_1,ENTITY_RE_2,ampRe,continuationMarker,cssSchema,decimalEscapeRe,endTagRe,entityLookupElement,gtRe,hexEscapeRe,html,looseAmpRe,ltRe,nulRe,parseCssDeclarations,quotRe,safeEntityNameRe,sanitizeCssProperty,splitWillCapture;'undefined'!==typeof
window&&(parseCssDeclarations=window['parseCssDeclarations'],sanitizeCssProperty=window['sanitizeCssProperty'],cssSchema=window['cssSchema']),ENTITIES={'lt':'\x3c','LT':'\x3c','gt':'\x3e','GT':'\x3e','amp':'\x26','AMP':'\x26','quot':'\"','apos':'\'','nbsp':'\xa0'},decimalEscapeRe=/^#(\d+)$/,hexEscapeRe=/^#x([0-9A-Fa-f]+)$/,safeEntityNameRe=/^[A-Za-z][A-za-z0-9]+$/,entityLookupElement='undefined'!==typeof
window&&window['document']?window['document'].createElement('textarea'):null;function
lookupEntity(name){var m,text;return ENTITIES.hasOwnProperty(name)?ENTITIES[name]:(m=name.match(decimalEscapeRe),m?String.fromCharCode(parseInt(m[1],10)):(m=name.match(hexEscapeRe))?String.fromCharCode(parseInt(m[1],16)):entityLookupElement&&safeEntityNameRe.test(name)?(entityLookupElement.innerHTML='\x26'+name+';',text=entityLookupElement.textContent,ENTITIES[name]=text,text):'\x26'+name+';')}function
decodeOneEntity(_,name){return lookupEntity(name)}nulRe=/\0/g;function stripNULs(s){return s.replace(nulRe,'')}ENTITY_RE_1=/\x26(#[0-9]+|#[xX][0-9A-Fa-f]+|\w+);/g,ENTITY_RE_2=/^(#[0-9]+|#[xX][0-9A-Fa-f]+|\w+);/;function
unescapeEntities(s){return s.replace(ENTITY_RE_1,decodeOneEntity)}ampRe=/\x26/g,looseAmpRe=/\x26([^a-z#]|#(?:[^0-9x]|x(?:[^0-9a-f]|$)|$)|$)/gi,ltRe=/[\x3c]/g,gtRe=/\x3e/g,quotRe=/\"/g;function
escapeAttrib(s){return(''+s).replace(ampRe,'\x26amp;').replace(ltRe,'\x26lt;').replace(gtRe,'\x26gt;').replace(quotRe,'\x26#34;')}function
normalizeRCData(rcdata){return rcdata.replace(looseAmpRe,'\x26amp;$1').replace(ltRe,'\x26lt;').replace(gtRe,'\x26gt;')}ATTR_RE=new
RegExp('^\\s*([-.:\\w]+)(?:\\s*(=)\\s*((\")[^\"]*(\"|$)|(\')[^\']*(\'|$)|(?=[a-z][-\\w]*\\s*=)|[^\"\'\\s]*))?','i'),splitWillCapture='a,b'.split(/(,)/).length===3,EFLAGS_TEXT=html4.eflags['CDATA']|html4.eflags['RCDATA'];function
makeSaxParser(handler){var hcopy={'cdata':handler.cdata||handler['cdata'],'comment':handler.comment||handler['comment'],'endDoc':handler.endDoc||handler['endDoc'],'endTag':handler.endTag||handler['endTag'],'pcdata':handler.pcdata||handler['pcdata'],'rcdata':handler.rcdata||handler['rcdata'],'startDoc':handler.startDoc||handler['startDoc'],'startTag':handler.startTag||handler['startTag']};return function(htmlText,param){return parse(htmlText,hcopy,param)}}continuationMarker={};function
parse(htmlText,handler,param){var parts=htmlSplit(htmlText),state={'noMoreGT':false,'noMoreEndComments':false},m,p,tagName;parseCPS(handler,parts,0,state,param)}function
continuationMaker(h,parts,initial,state,param){return function(){parseCPS(h,parts,initial,state,param)}}function
parseCPS(h,parts,initial,state,param){var comment,current,eflags,end,m,next,p,pos,tag,tagName;try{h.startDoc&&initial==0&&h.startDoc(param);for(pos=initial,end=parts.length;pos<end;){current=parts[pos++],next=parts[pos];switch(current){case'\x26':ENTITY_RE_2.test(next)?(h.pcdata&&h.pcdata('\x26'+next,param,continuationMarker,continuationMaker(h,parts,pos,state,param)),++pos):h.pcdata&&h.pcdata('\x26amp;',param,continuationMarker,continuationMaker(h,parts,pos,state,param));break;case'\x3c/':(m=/^([-\w:]+)[^\'\"]*/.exec(next))?m[0].length===next.length&&parts[pos+1]==='\x3e'?(pos+=2,tagName=m[1].toLowerCase(),h.endTag&&h.endTag(tagName,param,continuationMarker,continuationMaker(h,parts,pos,state,param))):(pos=parseEndTag(parts,pos,h,param,continuationMarker,state)):h.pcdata&&h.pcdata('\x26lt;/',param,continuationMarker,continuationMaker(h,parts,pos,state,param));break;case'\x3c':(m=/^([-\w:]+)\s*\/?/.exec(next))?m[0].length===next.length&&parts[pos+1]==='\x3e'?(pos+=2,tagName=m[1].toLowerCase(),h.startTag&&h.startTag(tagName,[],param,continuationMarker,continuationMaker(h,parts,pos,state,param)),eflags=html4.ELEMENTS[tagName],eflags&EFLAGS_TEXT&&(tag={'name':tagName,'next':pos,'eflags':eflags},pos=parseText(parts,tag,h,param,continuationMarker,state))):(pos=parseStartTag(parts,pos,h,param,continuationMarker,state)):h.pcdata&&h.pcdata('\x26lt;',param,continuationMarker,continuationMaker(h,parts,pos,state,param));break;case'\x3c!--':if(!state.noMoreEndComments){for(p=pos+1;p<end;++p)if(parts[p]==='\x3e'&&/--$/.test(parts[p-1]))break;p<end?(h.comment&&(comment=parts.slice(pos,p).join(''),h.comment(comment.substr(0,comment.length-2),param,continuationMarker,continuationMaker(h,parts,p+1,state,param))),pos=p+1):(state.noMoreEndComments=true)}state.noMoreEndComments&&(h.pcdata&&h.pcdata('\x26lt;!--',param,continuationMarker,continuationMaker(h,parts,pos,state,param)));break;case'\x3c!':if(!/^\w/.test(next))h.pcdata&&h.pcdata('\x26lt;!',param,continuationMarker,continuationMaker(h,parts,pos,state,param));else{if(!state.noMoreGT){for(p=pos+1;p<end;++p)if(parts[p]==='\x3e')break;p<end?(pos=p+1):(state.noMoreGT=true)}state.noMoreGT&&(h.pcdata&&h.pcdata('\x26lt;!',param,continuationMarker,continuationMaker(h,parts,pos,state,param)))}break;case'\x3c?':if(!state.noMoreGT){for(p=pos+1;p<end;++p)if(parts[p]==='\x3e')break;p<end?(pos=p+1):(state.noMoreGT=true)}state.noMoreGT&&(h.pcdata&&h.pcdata('\x26lt;?',param,continuationMarker,continuationMaker(h,parts,pos,state,param)));break;case'\x3e':h.pcdata&&h.pcdata('\x26gt;',param,continuationMarker,continuationMaker(h,parts,pos,state,param));break;case'':break;default:h.pcdata&&h.pcdata(current,param,continuationMarker,continuationMaker(h,parts,pos,state,param))}}h.endDoc&&h.endDoc(param)}catch(e){if(e!==continuationMarker)throw e}}function
htmlSplit(str){var re=/(\x3c\/|\x3c\!--|\x3c[!?]|[\x26\x3c\x3e])/g,lastPos,m,parts;str+='';if(splitWillCapture)return str.split(re);parts=[],lastPos=0;while((m=re.exec(str))!==null)parts.push(str.substring(lastPos,m.index)),parts.push(m[0]),lastPos=m.index+m[0].length;return parts.push(str.substring(lastPos)),parts}function
parseEndTag(parts,pos,h,param,continuationMarker,state){var tag=parseTagAndAttrs(parts,pos);return tag?(h.endTag&&h.endTag(tag.name,param,continuationMarker,continuationMaker(h,parts,pos,state,param)),tag.next):parts.length}function
parseStartTag(parts,pos,h,param,continuationMarker,state){var tag=parseTagAndAttrs(parts,pos);return tag?(h.startTag&&h.startTag(tag.name,tag.attrs,param,continuationMarker,continuationMaker(h,parts,tag.next,state,param)),tag.eflags&EFLAGS_TEXT?parseText(parts,tag,h,param,continuationMarker,state):tag.next):parts.length}endTagRe={};function
parseText(parts,tag,h,param,continuationMarker,state){var end=parts.length,buf,first,p,re;endTagRe.hasOwnProperty(tag.name)||(endTagRe[tag.name]=new
RegExp(('^'+tag.name+'(?:[\\s\\/]|$)'),'i')),re=endTagRe[tag.name],first=tag.next,p=tag.next+1;for(;p<end;++p)if(parts[p-1]==='\x3c/'&&re.test(parts[p]))break;p<end&&(p-=1),buf=parts.slice(first,p).join('');if(tag.eflags&html4.eflags['CDATA'])h.cdata&&h.cdata(buf,param,continuationMarker,continuationMaker(h,parts,p,state,param));else
if(tag.eflags&html4.eflags['RCDATA'])h.rcdata&&h.rcdata(normalizeRCData(buf),param,continuationMarker,continuationMaker(h,parts,p,state,param));else
throw new Error('bug');return p}function parseTagAndAttrs(parts,pos){var m=/^([-\w:]+)/.exec(parts[pos]),tag={},aName,aValue,abuf,attrs,buf,end,p,quote,sawQuote;tag.name=m[1].toLowerCase(),tag.eflags=html4.ELEMENTS[tag.name],buf=parts[pos].substr(m[0].length),p=pos+1,end=parts.length;for(;p<end;++p){if(parts[p]==='\x3e')break;buf+=parts[p]}if(end<=p)return;attrs=[];while(buf!==''){m=ATTR_RE.exec(buf);if(!m)buf=buf.replace(/^[\s\S][^a-z\s]*/,'');else
if(m[4]&&!m[5]||m[6]&&!m[7]){quote=m[4]||m[6],sawQuote=false,abuf=[buf,parts[p++]];for(;p<end;++p){if(sawQuote){if(parts[p]==='\x3e')break}else
if(0<=parts[p].indexOf(quote))sawQuote=true;abuf.push(parts[p])}if(end<=p)break;buf=abuf.join('');continue}else
aName=m[1].toLowerCase(),aValue=m[2]?decodeValue(m[3]):'',attrs.push(aName,aValue),buf=buf.substr(m[0].length)}return tag.attrs=attrs,tag.next=p+1,tag}function
decodeValue(v){var q=v.charCodeAt(0);return(q===34||q===39)&&(v=v.substr(1,v.length-2)),unescapeEntities(stripNULs(v))}function
makeHtmlSanitizer(tagPolicy){var emit=function(text,out){ignoring||out.push(text)},ignoring,stack;return makeSaxParser({'startDoc':function(_){stack=[],ignoring=false},'startTag':function(tagNameOrig,attribs,out){var
attribName,decision,eflagsOrig,eflagsRep,i,n,onStack,tagNameRep,value;if(ignoring)return;if(!html4.ELEMENTS.hasOwnProperty(tagNameOrig))return;eflagsOrig=html4.ELEMENTS[tagNameOrig];if(eflagsOrig&html4.eflags['FOLDABLE'])return;decision=tagPolicy(tagNameOrig,attribs);if(!decision)return ignoring=!(eflagsOrig&html4.eflags['EMPTY']),void
0;else if(typeof decision!=='object')throw new Error('tagPolicy did not return object (old API?)');if('attribs'in
decision)attribs=decision['attribs'];else throw new Error('tagPolicy gave no attribs');'tagName'in
decision?(tagNameRep=decision['tagName'],eflagsRep=html4.ELEMENTS[tagNameRep]):(tagNameRep=tagNameOrig,eflagsRep=eflagsOrig),eflagsOrig&html4.eflags['OPTIONAL_ENDTAG']&&(onStack=stack[stack.length-1],onStack&&onStack.orig===tagNameOrig&&(onStack.rep!==tagNameRep||tagNameOrig!==tagNameRep)&&out.push('\x3c/',onStack.rep,'\x3e')),eflagsOrig&html4.eflags['EMPTY']||stack.push({'orig':tagNameOrig,'rep':tagNameRep}),out.push('\x3c',tagNameRep);for(i=0,n=attribs.length;i<n;i+=2)attribName=attribs[i],value=attribs[i+1],value!==null&&value!==void
0&&out.push(' ',attribName,'=\"',escapeAttrib(value),'\"');out.push('\x3e'),eflagsOrig&html4.eflags['EMPTY']&&!(eflagsRep&html4.eflags['EMPTY'])&&out.push('\x3c/',tagNameRep,'\x3e')},'endTag':function(tagName,out){var
eflags,i,index,stackElOrigTag,stackElRepTag;if(ignoring)return ignoring=false,void
0;if(!html4.ELEMENTS.hasOwnProperty(tagName))return;eflags=html4.ELEMENTS[tagName];if(!(eflags&(html4.eflags['EMPTY']|html4.eflags['FOLDABLE']))){if(eflags&html4.eflags['OPTIONAL_ENDTAG'])for(index=stack.length;--index>=0;){stackElOrigTag=stack[index].orig;if(stackElOrigTag===tagName)break;if(!(html4.ELEMENTS[stackElOrigTag]&html4.eflags['OPTIONAL_ENDTAG']))return}else
for(index=stack.length;--index>=0;)if(stack[index].orig===tagName)break;if(index<0)return;for(i=stack.length;--i>index;)stackElRepTag=stack[i].rep,html4.ELEMENTS[stackElRepTag]&html4.eflags['OPTIONAL_ENDTAG']||out.push('\x3c/',stackElRepTag,'\x3e');index<stack.length&&(tagName=stack[index].rep),stack.length=index,out.push('\x3c/',tagName,'\x3e')}},'pcdata':emit,'rcdata':emit,'cdata':emit,'endDoc':function(out){for(;stack.length;--stack.length)out.push('\x3c/',stack[stack.length-1].rep,'\x3e')}})}ALLOWED_URI_SCHEMES=/^(?:https?|mailto)$/i;function
safeUri(uri,effect,ltype,hints,naiveUriRewriter){var parsed,safe;if(!naiveUriRewriter)return null;try{parsed=URI.parse(''+uri);if(parsed){if(!parsed.hasScheme()||ALLOWED_URI_SCHEMES.test(parsed.getScheme()))return safe=naiveUriRewriter(parsed,effect,ltype,hints),safe?safe.toString():null}}catch(e){return null}return null}function
log(logger,tagName,attribName,oldValue,newValue){var changed;attribName||logger(tagName+' removed',{'change':'removed','tagName':tagName}),oldValue!==newValue&&(changed='changed',oldValue&&!newValue?(changed='removed'):!oldValue&&newValue&&(changed='added'),logger(tagName+'.'+attribName+' '+changed,{'change':changed,'tagName':tagName,'attribName':attribName,'oldValue':oldValue,'newValue':newValue}))}function
lookupAttribute(map,tagName,attribName){var attribKey=tagName+'::'+attribName;return map.hasOwnProperty(attribKey)?map[attribKey]:(attribKey='*::'+attribName,map.hasOwnProperty(attribKey)?map[attribKey]:void
0)}function getAttributeType(tagName,attribName){return lookupAttribute(html4.ATTRIBS,tagName,attribName)}function
getLoaderType(tagName,attribName){return lookupAttribute(html4.LOADERTYPES,tagName,attribName)}function
getUriEffect(tagName,attribName){return lookupAttribute(html4.URIEFFECTS,tagName,attribName)}function
sanitizeAttribs(tagName,attribs,opt_naiveUriRewriter,opt_nmTokenPolicy,opt_logger){var
attribKey,attribName,atype,i,oldValue,sanitizedDeclarations,value;for(i=0;i<attribs.length;i+=2){attribName=attribs[i],value=attribs[i+1],oldValue=value,atype=null,((attribKey=tagName+'::'+attribName,html4.ATTRIBS.hasOwnProperty(attribKey))||(attribKey='*::'+attribName,html4.ATTRIBS.hasOwnProperty(attribKey)))&&(atype=html4.ATTRIBS[attribKey]);if(atype!==null)switch(atype){case
html4.atype['NONE']:break;case html4.atype['SCRIPT']:value=null,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break;case
html4.atype['STYLE']:if('undefined'===typeof parseCssDeclarations){value=null,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break}sanitizedDeclarations=[],parseCssDeclarations(value,{'declaration':function(property,tokens){var
normProp=property.toLowerCase(),schema=cssSchema[normProp];if(!schema)return;sanitizeCssProperty(normProp,schema,tokens,opt_naiveUriRewriter?function(url){return safeUri(url,html4.ueffects.SAME_DOCUMENT,html4.ltypes.SANDBOXED,{'TYPE':'CSS','CSS_PROP':normProp},opt_naiveUriRewriter)}:null),sanitizedDeclarations.push(property+': '+tokens.join(' '))}}),value=sanitizedDeclarations.length>0?sanitizedDeclarations.join(' ; '):null,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break;case
html4.atype['ID']:case html4.atype['IDREF']:case html4.atype['IDREFS']:case html4.atype['GLOBAL_NAME']:case
html4.atype['LOCAL_NAME']:case html4.atype['CLASSES']:value=opt_nmTokenPolicy?opt_nmTokenPolicy(value):value,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break;case
html4.atype['URI']:value=safeUri(value,getUriEffect(tagName,attribName),getLoaderType(tagName,attribName),{'TYPE':'MARKUP','XML_ATTR':attribName,'XML_TAG':tagName},opt_naiveUriRewriter),opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break;case
html4.atype['URI_FRAGMENT']:value&&'#'===value.charAt(0)?(value=value.substring(1),value=opt_nmTokenPolicy?opt_nmTokenPolicy(value):value,value!==null&&value!==void
0&&(value='#'+value)):(value=null),opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);break;default:value=null,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value)}else
value=null,opt_logger&&log(opt_logger,tagName,attribName,oldValue,value);attribs[i+1]=value}return attribs}function
makeTagPolicy(opt_naiveUriRewriter,opt_nmTokenPolicy,opt_logger){return function(tagName,attribs){if(!(html4.ELEMENTS[tagName]&html4.eflags['UNSAFE']))return{'attribs':sanitizeAttribs(tagName,attribs,opt_naiveUriRewriter,opt_nmTokenPolicy,opt_logger)};opt_logger&&log(opt_logger,tagName,undefined,undefined,undefined)}}function
sanitizeWithPolicy(inputHtml,tagPolicy){var outputArray=[];return makeHtmlSanitizer(tagPolicy)(inputHtml,outputArray),outputArray.join('')}function
sanitize(inputHtml,opt_naiveUriRewriter,opt_nmTokenPolicy,opt_logger){var tagPolicy=makeTagPolicy(opt_naiveUriRewriter,opt_nmTokenPolicy,opt_logger);return sanitizeWithPolicy(inputHtml,tagPolicy)}return html={},html.escapeAttrib=html['escapeAttrib']=escapeAttrib,html.makeHtmlSanitizer=html['makeHtmlSanitizer']=makeHtmlSanitizer,html.makeSaxParser=html['makeSaxParser']=makeSaxParser,html.makeTagPolicy=html['makeTagPolicy']=makeTagPolicy,html.normalizeRCData=html['normalizeRCData']=normalizeRCData,html.sanitize=html['sanitize']=sanitize,html.sanitizeAttribs=html['sanitizeAttribs']=sanitizeAttribs,html.sanitizeWithPolicy=html['sanitizeWithPolicy']=sanitizeWithPolicy,html.unescapeEntities=html['unescapeEntities']=unescapeEntities,html})(html4),html_sanitize=html['sanitize'],typeof
window!=='undefined'&&(window['html']=html,window['html_sanitize']=html_sanitize)}
/* $Date: 2007-06-12 18:02:31 $ */

// Handles encode/decode of ASCII and Unicode strings.

var UTF8 = {};
UTF8.encode = function(s) {
    var u = [];
    for (var i = 0; i < s.length; ++i) {
        var c = s.charCodeAt(i);
        if (c < 0x80) {
            u.push(c);
        } else if (c < 0x800) {
            u.push(0xC0 | (c >> 6));
            u.push(0x80 | (63 & c));
        } else if (c < 0x10000) {
            u.push(0xE0 | (c >> 12));
            u.push(0x80 | (63 & (c >> 6)));
            u.push(0x80 | (63 & c));
        } else {
            u.push(0xF0 | (c >> 18));
            u.push(0x80 | (63 & (c >> 12)));
            u.push(0x80 | (63 & (c >> 6)));
            u.push(0x80 | (63 & c));
        }
    }
    return u;
};
UTF8.decode = function(u) {
    var a = [];
    var i = 0;
    while (i < u.length) {
        var v = u[i++];
        if (v < 0x80) {
            // no need to mask byte
        } else if (v < 0xE0) {
            v = (31 & v) << 6;
            v |= (63 & u[i++]);
        } else if (v < 0xF0) {
            v = (15 & v) << 12;
            v |= (63 & u[i++]) << 6;
            v |= (63 & u[i++]);
        } else {
            v = (7 & v) << 18;
            v |= (63 & u[i++]) << 12;
            v |= (63 & u[i++]) << 6;
            v |= (63 & u[i++]);
        }
        a.push(String.fromCharCode(v));
    }
    return a.join('');
};

var BASE64 = {};
(function(T){
    var encodeArray = function(u) {
        var i = 0;
        var a = [];
        var n = 0 | (u.length / 3);
        while (0 < n--) {
            var v = (u[i] << 16) + (u[i+1] << 8) + u[i+2];
            i += 3;
            a.push(T.charAt(63 & (v >> 18)));
            a.push(T.charAt(63 & (v >> 12)));
            a.push(T.charAt(63 & (v >> 6)));
            a.push(T.charAt(63 & v));
        }
        if (2 == (u.length - i)) {
            var v = (u[i] << 16) + (u[i+1] << 8);
            a.push(T.charAt(63 & (v >> 18)));
            a.push(T.charAt(63 & (v >> 12)));
            a.push(T.charAt(63 & (v >> 6)));
            a.push('=');
        } else if (1 == (u.length - i)) {
            var v = (u[i] << 16);
            a.push(T.charAt(63 & (v >> 18)));
            a.push(T.charAt(63 & (v >> 12)));
            a.push('==');
        }
        return a.join('');
    }
    var R = (function(){
        var a = [];
        for (var i=0; i<T.length; ++i) {
            a[T.charCodeAt(i)] = i;
        }
        a['='.charCodeAt(0)] = 0;
        return a;
    })();
    var decodeArray = function(s) {
        var i = 0;
        var u = [];
        var n = 0 | (s.length / 4);
        while (0 < n--) {
            var v = (R[s.charCodeAt(i)] << 18) + (R[s.charCodeAt(i+1)] << 12) + (R[s.charCodeAt(i+2)] << 6) + R[s.charCodeAt(i+3)];
            i += 4;
            u.push(255 & (v >> 16));
            u.push(255 & (v >> 8));
            u.push(255 & v);
        }
        if (u) {
            if ('=' == s.charAt(i-2)) {
                u.pop();
                u.pop();
            } else if ('=' == s.charAt(i-1)) {
                u.pop();
            }
        }
        return u;
    }
    var ASCII = {};
    ASCII.encode = function(s) {
        var u = [];
        for (var i = 0; i<s.length; ++i) {
            u.push(s.charCodeAt(i));
        }
        return u;
    };
    ASCII.decode = function(u) {
        for (var i = 0; i<s.length; ++i) {
            a[i] = String.fromCharCode(a[i]);
        }
        return a.join('');
    };
    BASE64.encodeASCII = function(s) {
        var u = ASCII.encode(s);
        return encodeArray(u);
    };
    BASE64.decodeASCII = function(s) {
        var a = decodeArray(s);
        return ASCII.decode(a);
    };
    BASE64.encode = function(s) {
        var u = UTF8.encode(s);
        return encodeArray(u);
    };
    BASE64.decode = function(s) {
        var u = decodeArray(s);
        return UTF8.decode(u);
    };
})("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/");

if (undefined === btoa) {
    var btoa = BASE64.encode;
}
if (undefined === atob) {
    var atob = BASE64.decode;
}

(function() {
  var Translator, i18n, translator,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  Translator = (function() {
    function Translator() {
      this.translate = __bind(this.translate, this);      this.data = {
        values: {},
        contexts: []
      };
      this.globalContext = {};
    }

    Translator.prototype.translate = function(text, defaultNumOrFormatting, numOrFormattingOrContext, formattingOrContext, context) {
      var defaultText, formatting, isObject, num;

      if (context == null) {
        context = this.globalContext;
      }
      isObject = function(obj) {
        var type;

        type = typeof obj;
        return type === "function" || type === "object" && !!obj;
      };
      if (isObject(defaultNumOrFormatting)) {
        defaultText = null;
        num = null;
        formatting = defaultNumOrFormatting;
        context = numOrFormattingOrContext || this.globalContext;
      } else {
        if (typeof defaultNumOrFormatting === "number") {
          defaultText = null;
          num = defaultNumOrFormatting;
          formatting = numOrFormattingOrContext;
          context = formattingOrContext || this.globalContext;
        } else {
          defaultText = defaultNumOrFormatting;
          if (typeof numOrFormattingOrContext === "number") {
            num = numOrFormattingOrContext;
            formatting = formattingOrContext;
            context = context;
          } else {
            num = null;
            formatting = numOrFormattingOrContext;
            context = formattingOrContext || this.globalContext;
          }
        }
      }
      if (isObject(text)) {
        if (isObject(text['i18n'])) {
          text = text['i18n'];
        }
        return this.translateHash(text, context);
      } else {
        return this.translateText(text, num, formatting, context, defaultText);
      }
    };

    Translator.prototype.add = function(d) {
      var c, k, v, _i, _len, _ref, _ref1, _results;

      if ((d.values != null)) {
        _ref = d.values;
        for (k in _ref) {
          v = _ref[k];
          this.data.values[k] = v;
        }
      }
      if ((d.contexts != null)) {
        _ref1 = d.contexts;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          c = _ref1[_i];
          _results.push(this.data.contexts.push(c));
        }
        return _results;
      }
    };

    Translator.prototype.setContext = function(key, value) {
      return this.globalContext[key] = value;
    };

    Translator.prototype.clearContext = function(key) {
      return this.lobalContext[key] = null;
    };

    Translator.prototype.reset = function() {
      this.data = {
        values: {},
        contexts: []
      };
      return this.globalContext = {};
    };

    Translator.prototype.resetData = function() {
      return this.data = {
        values: {},
        contexts: []
      };
    };

    Translator.prototype.resetContext = function() {
      return this.globalContext = {};
    };

    Translator.prototype.translateHash = function(hash, context) {
      var k, v;

      for (k in hash) {
        v = hash[k];
        if (typeof v === "string") {
          hash[k] = this.translateText(v, null, null, context);
        }
      }
      return hash;
    };

    Translator.prototype.translateText = function(text, num, formatting, context, defaultText) {
      var contextData, result;

      if (context == null) {
        context = this.globalContext;
      }
      if (this.data == null) {
        return this.useOriginalText(defaultText || text, num, formatting);
      }
      contextData = this.getContextData(this.data, context);
      if (contextData != null) {
        result = this.findTranslation(text, num, formatting, contextData.values, defaultText);
      }
      if (result == null) {
        result = this.findTranslation(text, num, formatting, this.data.values, defaultText);
      }
      if (result == null) {
        return this.useOriginalText(defaultText || text, num, formatting);
      }
      return result;
    };

    Translator.prototype.findTranslation = function(text, num, formatting, data) {
      var result, triple, value, _i, _len;

      value = data[text];
      if (value == null) {
        return null;
      }
      if (num == null) {
        if (typeof value === "string") {
          return this.applyFormatting(value, num, formatting);
        }
      } else {
        if (value instanceof Array || value.length) {
          for (_i = 0, _len = value.length; _i < _len; _i++) {
            triple = value[_i];
            if ((num >= triple[0] || triple[0] === null) && (num <= triple[1] || triple[1] === null)) {
              result = this.applyFormatting(triple[2].replace("-%n", String(-num)), num, formatting);
              return this.applyFormatting(result.replace("%n", String(num)), num, formatting);
            }
          }
        }
      }
      return null;
    };

    Translator.prototype.getContextData = function(data, context) {
      var c, equal, key, value, _i, _len, _ref, _ref1;

      if (data.contexts == null) {
        return null;
      }
      _ref = data.contexts;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        c = _ref[_i];
        equal = true;
        _ref1 = c.matches;
        for (key in _ref1) {
          value = _ref1[key];
          equal = equal && value === context[key];
        }
        if (equal) {
          return c;
        }
      }
      return null;
    };

    Translator.prototype.useOriginalText = function(text, num, formatting) {
      if (num == null) {
        return this.applyFormatting(text, num, formatting);
      }
      return this.applyFormatting(text.replace("%n", String(num)), num, formatting);
    };

    Translator.prototype.applyFormatting = function(text, num, formatting) {
      var ind, regex;

      for (ind in formatting) {
        regex = new RegExp("%{" + ind + "}", "g");
        text = text.replace(regex, formatting[ind]);
      }
      return text;
    };

    return Translator;

  })();

  translator = new Translator();

  i18n = translator.translate;

  i18n.translator = translator;

  i18n.create = function(data) {
    var trans;

    trans = new Translator();
    if (data != null) {
      trans.add(data);
    }
    trans.translate.create = i18n.create;
    return trans.translate;
  };

  (typeof module !== "undefined" && module !== null ? module.exports = i18n : void 0) || (this.i18n = i18n);

}).call(this);
/*! For license information please see sanitizer.js.LICENSE.txt */
(()=>{var t={742:(t,e)=>{"use strict";e.byteLength=function(t){var e=c(t),r=e[0],i=e[1];return 3*(r+i)/4-i},e.toByteArray=function(t){var e,r,s=c(t),o=s[0],a=s[1],h=new n(function(t,e,r){return 3*(e+r)/4-r}(0,o,a)),u=0,l=a>0?o-4:o;for(r=0;r<l;r+=4)e=i[t.charCodeAt(r)]<<18|i[t.charCodeAt(r+1)]<<12|i[t.charCodeAt(r+2)]<<6|i[t.charCodeAt(r+3)],h[u++]=e>>16&255,h[u++]=e>>8&255,h[u++]=255&e;return 2===a&&(e=i[t.charCodeAt(r)]<<2|i[t.charCodeAt(r+1)]>>4,h[u++]=255&e),1===a&&(e=i[t.charCodeAt(r)]<<10|i[t.charCodeAt(r+1)]<<4|i[t.charCodeAt(r+2)]>>2,h[u++]=e>>8&255,h[u++]=255&e),h},e.fromByteArray=function(t){for(var e,i=t.length,n=i%3,s=[],o=16383,a=0,c=i-n;a<c;a+=o)s.push(h(t,a,a+o>c?c:a+o));return 1===n?(e=t[i-1],s.push(r[e>>2]+r[e<<4&63]+"==")):2===n&&(e=(t[i-2]<<8)+t[i-1],s.push(r[e>>10]+r[e>>4&63]+r[e<<2&63]+"=")),s.join("")};for(var r=[],i=[],n="undefined"!=typeof Uint8Array?Uint8Array:Array,s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",o=0,a=s.length;o<a;++o)r[o]=s[o],i[s.charCodeAt(o)]=o;function c(t){var e=t.length;if(e%4>0)throw new Error("Invalid string. Length must be a multiple of 4");var r=t.indexOf("=");return-1===r&&(r=e),[r,r===e?0:4-r%4]}function h(t,e,i){for(var n,s,o=[],a=e;a<i;a+=3)n=(t[a]<<16&16711680)+(t[a+1]<<8&65280)+(255&t[a+2]),o.push(r[(s=n)>>18&63]+r[s>>12&63]+r[s>>6&63]+r[63&s]);return o.join("")}i["-".charCodeAt(0)]=62,i["_".charCodeAt(0)]=63},764:(t,e,r)=>{"use strict";var i=r(742),n=r(645),s=r(826);function o(){return c.TYPED_ARRAY_SUPPORT?2147483647:1073741823}function a(t,e){if(o()<e)throw new RangeError("Invalid typed array length");return c.TYPED_ARRAY_SUPPORT?(t=new Uint8Array(e)).__proto__=c.prototype:(null===t&&(t=new c(e)),t.length=e),t}function c(t,e,r){if(!(c.TYPED_ARRAY_SUPPORT||this instanceof c))return new c(t,e,r);if("number"==typeof t){if("string"==typeof e)throw new Error("If encoding is specified then the first argument must be a string");return l(this,t)}return h(this,t,e,r)}function h(t,e,r,i){if("number"==typeof e)throw new TypeError('"value" argument must not be a number');return"undefined"!=typeof ArrayBuffer&&e instanceof ArrayBuffer?function(t,e,r,i){if(e.byteLength,r<0||e.byteLength<r)throw new RangeError("'offset' is out of bounds");if(e.byteLength<r+(i||0))throw new RangeError("'length' is out of bounds");return e=void 0===r&&void 0===i?new Uint8Array(e):void 0===i?new Uint8Array(e,r):new Uint8Array(e,r,i),c.TYPED_ARRAY_SUPPORT?(t=e).__proto__=c.prototype:t=p(t,e),t}(t,e,r,i):"string"==typeof e?function(t,e,r){if("string"==typeof r&&""!==r||(r="utf8"),!c.isEncoding(r))throw new TypeError('"encoding" must be a valid string encoding');var i=0|d(e,r),n=(t=a(t,i)).write(e,r);return n!==i&&(t=t.slice(0,n)),t}(t,e,r):function(t,e){if(c.isBuffer(e)){var r=0|f(e.length);return 0===(t=a(t,r)).length||e.copy(t,0,0,r),t}if(e){if("undefined"!=typeof ArrayBuffer&&e.buffer instanceof ArrayBuffer||"length"in e)return"number"!=typeof e.length||(i=e.length)!=i?a(t,0):p(t,e);if("Buffer"===e.type&&s(e.data))return p(t,e.data)}var i;throw new TypeError("First argument must be a string, Buffer, ArrayBuffer, Array, or array-like object.")}(t,e)}function u(t){if("number"!=typeof t)throw new TypeError('"size" argument must be a number');if(t<0)throw new RangeError('"size" argument must not be negative')}function l(t,e){if(u(e),t=a(t,e<0?0:0|f(e)),!c.TYPED_ARRAY_SUPPORT)for(var r=0;r<e;++r)t[r]=0;return t}function p(t,e){var r=e.length<0?0:0|f(e.length);t=a(t,r);for(var i=0;i<r;i+=1)t[i]=255&e[i];return t}function f(t){if(t>=o())throw new RangeError("Attempt to allocate Buffer larger than maximum size: 0x"+o().toString(16)+" bytes");return 0|t}function d(t,e){if(c.isBuffer(t))return t.length;if("undefined"!=typeof ArrayBuffer&&"function"==typeof ArrayBuffer.isView&&(ArrayBuffer.isView(t)||t instanceof ArrayBuffer))return t.byteLength;"string"!=typeof t&&(t=""+t);var r=t.length;if(0===r)return 0;for(var i=!1;;)switch(e){case"ascii":case"latin1":case"binary":return r;case"utf8":case"utf-8":case void 0:return V(t).length;case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return 2*r;case"hex":return r>>>1;case"base64":return j(t).length;default:if(i)return V(t).length;e=(""+e).toLowerCase(),i=!0}}function g(t,e,r){var i=!1;if((void 0===e||e<0)&&(e=0),e>this.length)return"";if((void 0===r||r>this.length)&&(r=this.length),r<=0)return"";if((r>>>=0)<=(e>>>=0))return"";for(t||(t="utf8");;)switch(t){case"hex":return k(this,e,r);case"utf8":case"utf-8":return T(this,e,r);case"ascii":return q(this,e,r);case"latin1":case"binary":return C(this,e,r);case"base64":return A(this,e,r);case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return N(this,e,r);default:if(i)throw new TypeError("Unknown encoding: "+t);t=(t+"").toLowerCase(),i=!0}}function _(t,e,r){var i=t[e];t[e]=t[r],t[r]=i}function m(t,e,r,i,n){if(0===t.length)return-1;if("string"==typeof r?(i=r,r=0):r>2147483647?r=2147483647:r<-2147483648&&(r=-2147483648),r=+r,isNaN(r)&&(r=n?0:t.length-1),r<0&&(r=t.length+r),r>=t.length){if(n)return-1;r=t.length-1}else if(r<0){if(!n)return-1;r=0}if("string"==typeof e&&(e=c.from(e,i)),c.isBuffer(e))return 0===e.length?-1:b(t,e,r,i,n);if("number"==typeof e)return e&=255,c.TYPED_ARRAY_SUPPORT&&"function"==typeof Uint8Array.prototype.indexOf?n?Uint8Array.prototype.indexOf.call(t,e,r):Uint8Array.prototype.lastIndexOf.call(t,e,r):b(t,[e],r,i,n);throw new TypeError("val must be string, number or Buffer")}function b(t,e,r,i,n){var s,o=1,a=t.length,c=e.length;if(void 0!==i&&("ucs2"===(i=String(i).toLowerCase())||"ucs-2"===i||"utf16le"===i||"utf-16le"===i)){if(t.length<2||e.length<2)return-1;o=2,a/=2,c/=2,r/=2}function h(t,e){return 1===o?t[e]:t.readUInt16BE(e*o)}if(n){var u=-1;for(s=r;s<a;s++)if(h(t,s)===h(e,-1===u?0:s-u)){if(-1===u&&(u=s),s-u+1===c)return u*o}else-1!==u&&(s-=s-u),u=-1}else for(r+c>a&&(r=a-c),s=r;s>=0;s--){for(var l=!0,p=0;p<c;p++)if(h(t,s+p)!==h(e,p)){l=!1;break}if(l)return s}return-1}function y(t,e,r,i){r=Number(r)||0;var n=t.length-r;i?(i=Number(i))>n&&(i=n):i=n;var s=e.length;if(s%2!=0)throw new TypeError("Invalid hex string");i>s/2&&(i=s/2);for(var o=0;o<i;++o){var a=parseInt(e.substr(2*o,2),16);if(isNaN(a))return o;t[r+o]=a}return o}function v(t,e,r,i){return H(V(e,t.length-r),t,r,i)}function w(t,e,r,i){return H(function(t){for(var e=[],r=0;r<t.length;++r)e.push(255&t.charCodeAt(r));return e}(e),t,r,i)}function x(t,e,r,i){return w(t,e,r,i)}function S(t,e,r,i){return H(j(e),t,r,i)}function E(t,e,r,i){return H(function(t,e){for(var r,i,n,s=[],o=0;o<t.length&&!((e-=2)<0);++o)i=(r=t.charCodeAt(o))>>8,n=r%256,s.push(n),s.push(i);return s}(e,t.length-r),t,r,i)}function A(t,e,r){return 0===e&&r===t.length?i.fromByteArray(t):i.fromByteArray(t.slice(e,r))}function T(t,e,r){r=Math.min(t.length,r);for(var i=[],n=e;n<r;){var s,o,a,c,h=t[n],u=null,l=h>239?4:h>223?3:h>191?2:1;if(n+l<=r)switch(l){case 1:h<128&&(u=h);break;case 2:128==(192&(s=t[n+1]))&&(c=(31&h)<<6|63&s)>127&&(u=c);break;case 3:s=t[n+1],o=t[n+2],128==(192&s)&&128==(192&o)&&(c=(15&h)<<12|(63&s)<<6|63&o)>2047&&(c<55296||c>57343)&&(u=c);break;case 4:s=t[n+1],o=t[n+2],a=t[n+3],128==(192&s)&&128==(192&o)&&128==(192&a)&&(c=(15&h)<<18|(63&s)<<12|(63&o)<<6|63&a)>65535&&c<1114112&&(u=c)}null===u?(u=65533,l=1):u>65535&&(u-=65536,i.push(u>>>10&1023|55296),u=56320|1023&u),i.push(u),n+=l}return function(t){var e=t.length;if(e<=L)return String.fromCharCode.apply(String,t);for(var r="",i=0;i<e;)r+=String.fromCharCode.apply(String,t.slice(i,i+=L));return r}(i)}e.Buffer=c,e.SlowBuffer=function(t){return+t!=t&&(t=0),c.alloc(+t)},e.INSPECT_MAX_BYTES=50,c.TYPED_ARRAY_SUPPORT=void 0!==r.g.TYPED_ARRAY_SUPPORT?r.g.TYPED_ARRAY_SUPPORT:function(){try{var t=new Uint8Array(1);return t.__proto__={__proto__:Uint8Array.prototype,foo:function(){return 42}},42===t.foo()&&"function"==typeof t.subarray&&0===t.subarray(1,1).byteLength}catch(t){return!1}}(),e.kMaxLength=o(),c.poolSize=8192,c._augment=function(t){return t.__proto__=c.prototype,t},c.from=function(t,e,r){return h(null,t,e,r)},c.TYPED_ARRAY_SUPPORT&&(c.prototype.__proto__=Uint8Array.prototype,c.__proto__=Uint8Array,"undefined"!=typeof Symbol&&Symbol.species&&c[Symbol.species]===c&&Object.defineProperty(c,Symbol.species,{value:null,configurable:!0})),c.alloc=function(t,e,r){return function(t,e,r,i){return u(e),e<=0?a(t,e):void 0!==r?"string"==typeof i?a(t,e).fill(r,i):a(t,e).fill(r):a(t,e)}(null,t,e,r)},c.allocUnsafe=function(t){return l(null,t)},c.allocUnsafeSlow=function(t){return l(null,t)},c.isBuffer=function(t){return!(null==t||!t._isBuffer)},c.compare=function(t,e){if(!c.isBuffer(t)||!c.isBuffer(e))throw new TypeError("Arguments must be Buffers");if(t===e)return 0;for(var r=t.length,i=e.length,n=0,s=Math.min(r,i);n<s;++n)if(t[n]!==e[n]){r=t[n],i=e[n];break}return r<i?-1:i<r?1:0},c.isEncoding=function(t){switch(String(t).toLowerCase()){case"hex":case"utf8":case"utf-8":case"ascii":case"latin1":case"binary":case"base64":case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return!0;default:return!1}},c.concat=function(t,e){if(!s(t))throw new TypeError('"list" argument must be an Array of Buffers');if(0===t.length)return c.alloc(0);var r;if(void 0===e)for(e=0,r=0;r<t.length;++r)e+=t[r].length;var i=c.allocUnsafe(e),n=0;for(r=0;r<t.length;++r){var o=t[r];if(!c.isBuffer(o))throw new TypeError('"list" argument must be an Array of Buffers');o.copy(i,n),n+=o.length}return i},c.byteLength=d,c.prototype._isBuffer=!0,c.prototype.swap16=function(){var t=this.length;if(t%2!=0)throw new RangeError("Buffer size must be a multiple of 16-bits");for(var e=0;e<t;e+=2)_(this,e,e+1);return this},c.prototype.swap32=function(){var t=this.length;if(t%4!=0)throw new RangeError("Buffer size must be a multiple of 32-bits");for(var e=0;e<t;e+=4)_(this,e,e+3),_(this,e+1,e+2);return this},c.prototype.swap64=function(){var t=this.length;if(t%8!=0)throw new RangeError("Buffer size must be a multiple of 64-bits");for(var e=0;e<t;e+=8)_(this,e,e+7),_(this,e+1,e+6),_(this,e+2,e+5),_(this,e+3,e+4);return this},c.prototype.toString=function(){var t=0|this.length;return 0===t?"":0===arguments.length?T(this,0,t):g.apply(this,arguments)},c.prototype.equals=function(t){if(!c.isBuffer(t))throw new TypeError("Argument must be a Buffer");return this===t||0===c.compare(this,t)},c.prototype.inspect=function(){var t="",r=e.INSPECT_MAX_BYTES;return this.length>0&&(t=this.toString("hex",0,r).match(/.{2}/g).join(" "),this.length>r&&(t+=" ... ")),"<Buffer "+t+">"},c.prototype.compare=function(t,e,r,i,n){if(!c.isBuffer(t))throw new TypeError("Argument must be a Buffer");if(void 0===e&&(e=0),void 0===r&&(r=t?t.length:0),void 0===i&&(i=0),void 0===n&&(n=this.length),e<0||r>t.length||i<0||n>this.length)throw new RangeError("out of range index");if(i>=n&&e>=r)return 0;if(i>=n)return-1;if(e>=r)return 1;if(this===t)return 0;for(var s=(n>>>=0)-(i>>>=0),o=(r>>>=0)-(e>>>=0),a=Math.min(s,o),h=this.slice(i,n),u=t.slice(e,r),l=0;l<a;++l)if(h[l]!==u[l]){s=h[l],o=u[l];break}return s<o?-1:o<s?1:0},c.prototype.includes=function(t,e,r){return-1!==this.indexOf(t,e,r)},c.prototype.indexOf=function(t,e,r){return m(this,t,e,r,!0)},c.prototype.lastIndexOf=function(t,e,r){return m(this,t,e,r,!1)},c.prototype.write=function(t,e,r,i){if(void 0===e)i="utf8",r=this.length,e=0;else if(void 0===r&&"string"==typeof e)i=e,r=this.length,e=0;else{if(!isFinite(e))throw new Error("Buffer.write(string, encoding, offset[, length]) is no longer supported");e|=0,isFinite(r)?(r|=0,void 0===i&&(i="utf8")):(i=r,r=void 0)}var n=this.length-e;if((void 0===r||r>n)&&(r=n),t.length>0&&(r<0||e<0)||e>this.length)throw new RangeError("Attempt to write outside buffer bounds");i||(i="utf8");for(var s=!1;;)switch(i){case"hex":return y(this,t,e,r);case"utf8":case"utf-8":return v(this,t,e,r);case"ascii":return w(this,t,e,r);case"latin1":case"binary":return x(this,t,e,r);case"base64":return S(this,t,e,r);case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return E(this,t,e,r);default:if(s)throw new TypeError("Unknown encoding: "+i);i=(""+i).toLowerCase(),s=!0}},c.prototype.toJSON=function(){return{type:"Buffer",data:Array.prototype.slice.call(this._arr||this,0)}};var L=4096;function q(t,e,r){var i="";r=Math.min(t.length,r);for(var n=e;n<r;++n)i+=String.fromCharCode(127&t[n]);return i}function C(t,e,r){var i="";r=Math.min(t.length,r);for(var n=e;n<r;++n)i+=String.fromCharCode(t[n]);return i}function k(t,e,r){var i,n=t.length;(!e||e<0)&&(e=0),(!r||r<0||r>n)&&(r=n);for(var s="",o=e;o<r;++o)s+=(i=t[o])<16?"0"+i.toString(16):i.toString(16);return s}function N(t,e,r){for(var i=t.slice(e,r),n="",s=0;s<i.length;s+=2)n+=String.fromCharCode(i[s]+256*i[s+1]);return n}function D(t,e,r){if(t%1!=0||t<0)throw new RangeError("offset is not uint");if(t+e>r)throw new RangeError("Trying to access beyond buffer length")}function B(t,e,r,i,n,s){if(!c.isBuffer(t))throw new TypeError('"buffer" argument must be a Buffer instance');if(e>n||e<s)throw new RangeError('"value" argument is out of bounds');if(r+i>t.length)throw new RangeError("Index out of range")}function R(t,e,r,i){e<0&&(e=65535+e+1);for(var n=0,s=Math.min(t.length-r,2);n<s;++n)t[r+n]=(e&255<<8*(i?n:1-n))>>>8*(i?n:1-n)}function O(t,e,r,i){e<0&&(e=4294967295+e+1);for(var n=0,s=Math.min(t.length-r,4);n<s;++n)t[r+n]=e>>>8*(i?n:3-n)&255}function I(t,e,r,i,n,s){if(r+i>t.length)throw new RangeError("Index out of range");if(r<0)throw new RangeError("Index out of range")}function P(t,e,r,i,s){return s||I(t,0,r,4),n.write(t,e,r,i,23,4),r+4}function U(t,e,r,i,s){return s||I(t,0,r,8),n.write(t,e,r,i,52,8),r+8}c.prototype.slice=function(t,e){var r,i=this.length;if((t=~~t)<0?(t+=i)<0&&(t=0):t>i&&(t=i),(e=void 0===e?i:~~e)<0?(e+=i)<0&&(e=0):e>i&&(e=i),e<t&&(e=t),c.TYPED_ARRAY_SUPPORT)(r=this.subarray(t,e)).__proto__=c.prototype;else{var n=e-t;r=new c(n,void 0);for(var s=0;s<n;++s)r[s]=this[s+t]}return r},c.prototype.readUIntLE=function(t,e,r){t|=0,e|=0,r||D(t,e,this.length);for(var i=this[t],n=1,s=0;++s<e&&(n*=256);)i+=this[t+s]*n;return i},c.prototype.readUIntBE=function(t,e,r){t|=0,e|=0,r||D(t,e,this.length);for(var i=this[t+--e],n=1;e>0&&(n*=256);)i+=this[t+--e]*n;return i},c.prototype.readUInt8=function(t,e){return e||D(t,1,this.length),this[t]},c.prototype.readUInt16LE=function(t,e){return e||D(t,2,this.length),this[t]|this[t+1]<<8},c.prototype.readUInt16BE=function(t,e){return e||D(t,2,this.length),this[t]<<8|this[t+1]},c.prototype.readUInt32LE=function(t,e){return e||D(t,4,this.length),(this[t]|this[t+1]<<8|this[t+2]<<16)+16777216*this[t+3]},c.prototype.readUInt32BE=function(t,e){return e||D(t,4,this.length),16777216*this[t]+(this[t+1]<<16|this[t+2]<<8|this[t+3])},c.prototype.readIntLE=function(t,e,r){t|=0,e|=0,r||D(t,e,this.length);for(var i=this[t],n=1,s=0;++s<e&&(n*=256);)i+=this[t+s]*n;return i>=(n*=128)&&(i-=Math.pow(2,8*e)),i},c.prototype.readIntBE=function(t,e,r){t|=0,e|=0,r||D(t,e,this.length);for(var i=e,n=1,s=this[t+--i];i>0&&(n*=256);)s+=this[t+--i]*n;return s>=(n*=128)&&(s-=Math.pow(2,8*e)),s},c.prototype.readInt8=function(t,e){return e||D(t,1,this.length),128&this[t]?-1*(255-this[t]+1):this[t]},c.prototype.readInt16LE=function(t,e){e||D(t,2,this.length);var r=this[t]|this[t+1]<<8;return 32768&r?4294901760|r:r},c.prototype.readInt16BE=function(t,e){e||D(t,2,this.length);var r=this[t+1]|this[t]<<8;return 32768&r?4294901760|r:r},c.prototype.readInt32LE=function(t,e){return e||D(t,4,this.length),this[t]|this[t+1]<<8|this[t+2]<<16|this[t+3]<<24},c.prototype.readInt32BE=function(t,e){return e||D(t,4,this.length),this[t]<<24|this[t+1]<<16|this[t+2]<<8|this[t+3]},c.prototype.readFloatLE=function(t,e){return e||D(t,4,this.length),n.read(this,t,!0,23,4)},c.prototype.readFloatBE=function(t,e){return e||D(t,4,this.length),n.read(this,t,!1,23,4)},c.prototype.readDoubleLE=function(t,e){return e||D(t,8,this.length),n.read(this,t,!0,52,8)},c.prototype.readDoubleBE=function(t,e){return e||D(t,8,this.length),n.read(this,t,!1,52,8)},c.prototype.writeUIntLE=function(t,e,r,i){t=+t,e|=0,r|=0,i||B(this,t,e,r,Math.pow(2,8*r)-1,0);var n=1,s=0;for(this[e]=255&t;++s<r&&(n*=256);)this[e+s]=t/n&255;return e+r},c.prototype.writeUIntBE=function(t,e,r,i){t=+t,e|=0,r|=0,i||B(this,t,e,r,Math.pow(2,8*r)-1,0);var n=r-1,s=1;for(this[e+n]=255&t;--n>=0&&(s*=256);)this[e+n]=t/s&255;return e+r},c.prototype.writeUInt8=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,1,255,0),c.TYPED_ARRAY_SUPPORT||(t=Math.floor(t)),this[e]=255&t,e+1},c.prototype.writeUInt16LE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,2,65535,0),c.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8):R(this,t,e,!0),e+2},c.prototype.writeUInt16BE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,2,65535,0),c.TYPED_ARRAY_SUPPORT?(this[e]=t>>>8,this[e+1]=255&t):R(this,t,e,!1),e+2},c.prototype.writeUInt32LE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,4,4294967295,0),c.TYPED_ARRAY_SUPPORT?(this[e+3]=t>>>24,this[e+2]=t>>>16,this[e+1]=t>>>8,this[e]=255&t):O(this,t,e,!0),e+4},c.prototype.writeUInt32BE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,4,4294967295,0),c.TYPED_ARRAY_SUPPORT?(this[e]=t>>>24,this[e+1]=t>>>16,this[e+2]=t>>>8,this[e+3]=255&t):O(this,t,e,!1),e+4},c.prototype.writeIntLE=function(t,e,r,i){if(t=+t,e|=0,!i){var n=Math.pow(2,8*r-1);B(this,t,e,r,n-1,-n)}var s=0,o=1,a=0;for(this[e]=255&t;++s<r&&(o*=256);)t<0&&0===a&&0!==this[e+s-1]&&(a=1),this[e+s]=(t/o>>0)-a&255;return e+r},c.prototype.writeIntBE=function(t,e,r,i){if(t=+t,e|=0,!i){var n=Math.pow(2,8*r-1);B(this,t,e,r,n-1,-n)}var s=r-1,o=1,a=0;for(this[e+s]=255&t;--s>=0&&(o*=256);)t<0&&0===a&&0!==this[e+s+1]&&(a=1),this[e+s]=(t/o>>0)-a&255;return e+r},c.prototype.writeInt8=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,1,127,-128),c.TYPED_ARRAY_SUPPORT||(t=Math.floor(t)),t<0&&(t=255+t+1),this[e]=255&t,e+1},c.prototype.writeInt16LE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,2,32767,-32768),c.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8):R(this,t,e,!0),e+2},c.prototype.writeInt16BE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,2,32767,-32768),c.TYPED_ARRAY_SUPPORT?(this[e]=t>>>8,this[e+1]=255&t):R(this,t,e,!1),e+2},c.prototype.writeInt32LE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,4,2147483647,-2147483648),c.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8,this[e+2]=t>>>16,this[e+3]=t>>>24):O(this,t,e,!0),e+4},c.prototype.writeInt32BE=function(t,e,r){return t=+t,e|=0,r||B(this,t,e,4,2147483647,-2147483648),t<0&&(t=4294967295+t+1),c.TYPED_ARRAY_SUPPORT?(this[e]=t>>>24,this[e+1]=t>>>16,this[e+2]=t>>>8,this[e+3]=255&t):O(this,t,e,!1),e+4},c.prototype.writeFloatLE=function(t,e,r){return P(this,t,e,!0,r)},c.prototype.writeFloatBE=function(t,e,r){return P(this,t,e,!1,r)},c.prototype.writeDoubleLE=function(t,e,r){return U(this,t,e,!0,r)},c.prototype.writeDoubleBE=function(t,e,r){return U(this,t,e,!1,r)},c.prototype.copy=function(t,e,r,i){if(r||(r=0),i||0===i||(i=this.length),e>=t.length&&(e=t.length),e||(e=0),i>0&&i<r&&(i=r),i===r)return 0;if(0===t.length||0===this.length)return 0;if(e<0)throw new RangeError("targetStart out of bounds");if(r<0||r>=this.length)throw new RangeError("sourceStart out of bounds");if(i<0)throw new RangeError("sourceEnd out of bounds");i>this.length&&(i=this.length),t.length-e<i-r&&(i=t.length-e+r);var n,s=i-r;if(this===t&&r<e&&e<i)for(n=s-1;n>=0;--n)t[n+e]=this[n+r];else if(s<1e3||!c.TYPED_ARRAY_SUPPORT)for(n=0;n<s;++n)t[n+e]=this[n+r];else Uint8Array.prototype.set.call(t,this.subarray(r,r+s),e);return s},c.prototype.fill=function(t,e,r,i){if("string"==typeof t){if("string"==typeof e?(i=e,e=0,r=this.length):"string"==typeof r&&(i=r,r=this.length),1===t.length){var n=t.charCodeAt(0);n<256&&(t=n)}if(void 0!==i&&"string"!=typeof i)throw new TypeError("encoding must be a string");if("string"==typeof i&&!c.isEncoding(i))throw new TypeError("Unknown encoding: "+i)}else"number"==typeof t&&(t&=255);if(e<0||this.length<e||this.length<r)throw new RangeError("Out of range index");if(r<=e)return this;var s;if(e>>>=0,r=void 0===r?this.length:r>>>0,t||(t=0),"number"==typeof t)for(s=e;s<r;++s)this[s]=t;else{var o=c.isBuffer(t)?t:V(new c(t,i).toString()),a=o.length;for(s=0;s<r-e;++s)this[s+e]=o[s%a]}return this};var M=/[^+\/0-9A-Za-z-_]/g;function V(t,e){var r;e=e||1/0;for(var i=t.length,n=null,s=[],o=0;o<i;++o){if((r=t.charCodeAt(o))>55295&&r<57344){if(!n){if(r>56319){(e-=3)>-1&&s.push(239,191,189);continue}if(o+1===i){(e-=3)>-1&&s.push(239,191,189);continue}n=r;continue}if(r<56320){(e-=3)>-1&&s.push(239,191,189),n=r;continue}r=65536+(n-55296<<10|r-56320)}else n&&(e-=3)>-1&&s.push(239,191,189);if(n=null,r<128){if((e-=1)<0)break;s.push(r)}else if(r<2048){if((e-=2)<0)break;s.push(r>>6|192,63&r|128)}else if(r<65536){if((e-=3)<0)break;s.push(r>>12|224,r>>6&63|128,63&r|128)}else{if(!(r<1114112))throw new Error("Invalid code point");if((e-=4)<0)break;s.push(r>>18|240,r>>12&63|128,r>>6&63|128,63&r|128)}}return s}function j(t){return i.toByteArray(function(t){if((t=function(t){return t.trim?t.trim():t.replace(/^\s+|\s+$/g,"")}(t).replace(M,"")).length<2)return"";for(;t.length%4!=0;)t+="=";return t}(t))}function H(t,e,r,i){for(var n=0;n<i&&!(n+r>=e.length||n>=t.length);++n)e[n+r]=t[n];return n}},138:(t,e,r)=>{var i=r(431),n=r(91),s={__proto__:null,style:!0,script:!0,xmp:!0,iframe:!0,noembed:!0,noframes:!0,plaintext:!0,noscript:!0},o={__proto__:null,area:!0,base:!0,basefont:!0,br:!0,col:!0,command:!0,embed:!0,frame:!0,hr:!0,img:!0,input:!0,isindex:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0},a=t.exports=function(t,e){Array.isArray(t)||t.cheerio||(t=[t]),e=e||{};for(var r="",n=0;n<t.length;n++){var s=t[n];"root"===s.type?r+=a(s.children,e):i.isTag(s)?r+=c(s,e):s.type===i.Directive?r+=h(s):s.type===i.Comment?r+=p(s):s.type===i.CDATA?r+=l(s):r+=u(s,e)}return r};function c(t,e){"svg"===t.name&&(e={decodeEntities:e.decodeEntities,xmlMode:!0});var r="<"+t.name,i=function(t,e){if(t){var r,i="";for(var s in t)i&&(i+=" "),i+=s,(null!==(r=t[s])&&""!==r||e.xmlMode)&&(i+='="'+(e.decodeEntities?n.encodeXML(r):r)+'"');return i}}(t.attribs,e);return i&&(r+=" "+i),!e.xmlMode||t.children&&0!==t.children.length?(r+=">",t.children&&(r+=a(t.children,e)),o[t.name]&&!e.xmlMode||(r+="</"+t.name+">")):r+="/>",r}function h(t){return"<"+t.data+">"}function u(t,e){var r=t.data||"";return!e.decodeEntities||t.parent&&t.parent.name in s||(r=n.encodeXML(r)),r}function l(t){return"<![CDATA["+t.children[0].data+"]]>"}function p(t){return"\x3c!--"+t.data+"--\x3e"}},431:t=>{t.exports={Text:"text",Directive:"directive",Comment:"comment",Script:"script",Style:"style",Tag:"tag",CDATA:"cdata",Doctype:"doctype",isTag:function(t){return"tag"===t.type||"script"===t.type||"style"===t.type}}},753:(t,e,r)=>{var i=r(431),n=/\s+/g,s=r(790),o=r(407);function a(t,e,r){"object"==typeof t?(r=e,e=t,t=null):"function"==typeof e&&(r=e,e=c),this._callback=t,this._options=e||c,this._elementCB=r,this.dom=[],this._done=!1,this._tagStack=[],this._parser=this._parser||null}var c={normalizeWhitespace:!1,withStartIndices:!1,withEndIndices:!1};a.prototype.onparserinit=function(t){this._parser=t},a.prototype.onreset=function(){a.call(this,this._callback,this._options,this._elementCB)},a.prototype.onend=function(){this._done||(this._done=!0,this._parser=null,this._handleCallback(null))},a.prototype._handleCallback=a.prototype.onerror=function(t){if("function"==typeof this._callback)this._callback(t,this.dom);else if(t)throw t},a.prototype.onclosetag=function(){var t=this._tagStack.pop();this._options.withEndIndices&&t&&(t.endIndex=this._parser.endIndex),this._elementCB&&this._elementCB(t)},a.prototype._createDomElement=function(t){if(!this._options.withDomLvl1)return t;var e;for(var r in e="tag"===t.type?Object.create(o):Object.create(s),t)t.hasOwnProperty(r)&&(e[r]=t[r]);return e},a.prototype._addDomElement=function(t){var e=this._tagStack[this._tagStack.length-1],r=e?e.children:this.dom,i=r[r.length-1];t.next=null,this._options.withStartIndices&&(t.startIndex=this._parser.startIndex),this._options.withEndIndices&&(t.endIndex=this._parser.endIndex),i?(t.prev=i,i.next=t):t.prev=null,r.push(t),t.parent=e||null},a.prototype.onopentag=function(t,e){var r={type:"script"===t?i.Script:"style"===t?i.Style:i.Tag,name:t,attribs:e,children:[]},n=this._createDomElement(r);this._addDomElement(n),this._tagStack.push(n)},a.prototype.ontext=function(t){var e,r=this._options.normalizeWhitespace||this._options.ignoreWhitespace;if(!this._tagStack.length&&this.dom.length&&(e=this.dom[this.dom.length-1]).type===i.Text)r?e.data=(e.data+t).replace(n," "):e.data+=t;else if(this._tagStack.length&&(e=this._tagStack[this._tagStack.length-1])&&(e=e.children[e.children.length-1])&&e.type===i.Text)r?e.data=(e.data+t).replace(n," "):e.data+=t;else{r&&(t=t.replace(n," "));var s=this._createDomElement({data:t,type:i.Text});this._addDomElement(s)}},a.prototype.oncomment=function(t){var e=this._tagStack[this._tagStack.length-1];if(e&&e.type===i.Comment)e.data+=t;else{var r={data:t,type:i.Comment},n=this._createDomElement(r);this._addDomElement(n),this._tagStack.push(n)}},a.prototype.oncdatastart=function(){var t={children:[{data:"",type:i.Text}],type:i.CDATA},e=this._createDomElement(t);this._addDomElement(e),this._tagStack.push(e)},a.prototype.oncommentend=a.prototype.oncdataend=function(){this._tagStack.pop()},a.prototype.onprocessinginstruction=function(t,e){var r=this._createDomElement({name:t,data:e,type:i.Directive});this._addDomElement(r)},t.exports=a},407:(t,e,r)=>{var i=r(790),n=t.exports=Object.create(i),s={tagName:"name"};Object.keys(s).forEach((function(t){var e=s[t];Object.defineProperty(n,t,{get:function(){return this[e]||null},set:function(t){return this[e]=t,t}})}))},790:t=>{var e=t.exports={get firstChild(){var t=this.children;return t&&t[0]||null},get lastChild(){var t=this.children;return t&&t[t.length-1]||null},get nodeType(){return i[this.type]||i.element}},r={tagName:"name",childNodes:"children",parentNode:"parent",previousSibling:"prev",nextSibling:"next",nodeValue:"data"},i={element:1,text:3,cdata:4,comment:8};Object.keys(r).forEach((function(t){var i=r[t];Object.defineProperty(e,t,{get:function(){return this[i]||null},set:function(t){return this[i]=t,t}})}))},417:(t,e,r)=>{var i=t.exports;[r(346),r(10),r(765),r(43),r(905),r(975)].forEach((function(t){Object.keys(t).forEach((function(e){i[e]=t[e].bind(i)}))}))},975:(t,e)=>{e.removeSubsets=function(t){for(var e,r,i,n=t.length;--n>-1;){for(e=r=t[n],t[n]=null,i=!0;r;){if(t.indexOf(r)>-1){i=!1,t.splice(n,1);break}r=r.parent}i&&(t[n]=e)}return t};var r=e.compareDocumentPosition=function(t,e){var r,i,n,s,o,a,c=[],h=[];if(t===e)return 0;for(r=t;r;)c.unshift(r),r=r.parent;for(r=e;r;)h.unshift(r),r=r.parent;for(a=0;c[a]===h[a];)a++;return 0===a?1:(n=(i=c[a-1]).children,s=c[a],o=h[a],n.indexOf(s)>n.indexOf(o)?i===e?20:4:i===t?10:2)};e.uniqueSort=function(t){var e,i,n=t.length;for(t=t.slice();--n>-1;)e=t[n],(i=t.indexOf(e))>-1&&i<n&&t.splice(n,1);return t.sort((function(t,e){var i=r(t,e);return 2&i?-1:4&i?1:0})),t}},905:(t,e,r)=>{var i=r(431),n=e.isTag=i.isTag;e.testElement=function(t,e){for(var r in t)if(t.hasOwnProperty(r))if("tag_name"===r){if(!n(e)||!t.tag_name(e.name))return!1}else if("tag_type"===r){if(!t.tag_type(e.type))return!1}else if("tag_contains"===r){if(n(e)||!t.tag_contains(e.data))return!1}else if(!e.attribs||!t[r](e.attribs[r]))return!1;return!0};var s={tag_name:function(t){return"function"==typeof t?function(e){return n(e)&&t(e.name)}:"*"===t?n:function(e){return n(e)&&e.name===t}},tag_type:function(t){return"function"==typeof t?function(e){return t(e.type)}:function(e){return e.type===t}},tag_contains:function(t){return"function"==typeof t?function(e){return!n(e)&&t(e.data)}:function(e){return!n(e)&&e.data===t}}};function o(t,e){return"function"==typeof e?function(r){return r.attribs&&e(r.attribs[t])}:function(r){return r.attribs&&r.attribs[t]===e}}function a(t,e){return function(r){return t(r)||e(r)}}e.getElements=function(t,e,r,i){var n=Object.keys(t).map((function(e){var r=t[e];return e in s?s[e](r):o(e,r)}));return 0===n.length?[]:this.filter(n.reduce(a),e,r,i)},e.getElementById=function(t,e,r){return Array.isArray(e)||(e=[e]),this.findOne(o("id",t),e,!1!==r)},e.getElementsByTagName=function(t,e,r,i){return this.filter(s.tag_name(t),e,r,i)},e.getElementsByTagType=function(t,e,r,i){return this.filter(s.tag_type(t),e,r,i)}},765:(t,e)=>{e.removeElement=function(t){if(t.prev&&(t.prev.next=t.next),t.next&&(t.next.prev=t.prev),t.parent){var e=t.parent.children;e.splice(e.lastIndexOf(t),1)}},e.replaceElement=function(t,e){var r=e.prev=t.prev;r&&(r.next=e);var i=e.next=t.next;i&&(i.prev=e);var n=e.parent=t.parent;if(n){var s=n.children;s[s.lastIndexOf(t)]=e}},e.appendChild=function(t,e){if(e.parent=t,1!==t.children.push(e)){var r=t.children[t.children.length-2];r.next=e,e.prev=r,e.next=null}},e.append=function(t,e){var r=t.parent,i=t.next;if(e.next=i,e.prev=t,t.next=e,e.parent=r,i){if(i.prev=e,r){var n=r.children;n.splice(n.lastIndexOf(i),0,e)}}else r&&r.children.push(e)},e.prepend=function(t,e){var r=t.parent;if(r){var i=r.children;i.splice(i.lastIndexOf(t),0,e)}t.prev&&(t.prev.next=e),e.parent=r,e.prev=t.prev,e.next=t,t.prev=e}},43:(t,e,r)=>{var i=r(431).isTag;function n(t,e,r,i){for(var s,o=[],a=0,c=e.length;a<c&&!(t(e[a])&&(o.push(e[a]),--i<=0))&&(s=e[a].children,!(r&&s&&s.length>0&&(s=n(t,s,r,i),o=o.concat(s),(i-=s.length)<=0)));a++);return o}t.exports={filter:function(t,e,r,i){return Array.isArray(e)||(e=[e]),"number"==typeof i&&isFinite(i)||(i=1/0),n(t,e,!1!==r,i)},find:n,findOneChild:function(t,e){for(var r=0,i=e.length;r<i;r++)if(t(e[r]))return e[r];return null},findOne:function t(e,r){for(var n=null,s=0,o=r.length;s<o&&!n;s++)i(r[s])&&(e(r[s])?n=r[s]:r[s].children.length>0&&(n=t(e,r[s].children)));return n},existsOne:function t(e,r){for(var n=0,s=r.length;n<s;n++)if(i(r[n])&&(e(r[n])||r[n].children.length>0&&t(e,r[n].children)))return!0;return!1},findAll:function(t,e){for(var r=[],n=e.slice();n.length;){var s=n.shift();i(s)&&(s.children&&s.children.length>0&&n.unshift.apply(n,s.children),t(s)&&r.push(s))}return r}}},346:(t,e,r)=>{var i=r(431),n=r(138),s=i.isTag;t.exports={getInnerHTML:function(t,e){return t.children?t.children.map((function(t){return n(t,e)})).join(""):""},getOuterHTML:n,getText:function t(e){return Array.isArray(e)?e.map(t).join(""):s(e)?"br"===e.name?"\n":t(e.children):e.type===i.CDATA?t(e.children):e.type===i.Text?e.data:""}}},10:(t,e)=>{var r=e.getChildren=function(t){return t.children},i=e.getParent=function(t){return t.parent};e.getSiblings=function(t){var e=i(t);return e?r(e):[t]},e.getAttributeValue=function(t,e){return t.attribs&&t.attribs[e]},e.hasAttrib=function(t,e){return!!t.attribs&&hasOwnProperty.call(t.attribs,e)},e.getName=function(t){return t.name}},91:(t,e,r)=>{var i=r(322),n=r(194);e.decode=function(t,e){return(!e||e<=0?n.XML:n.HTML)(t)},e.decodeStrict=function(t,e){return(!e||e<=0?n.XML:n.HTMLStrict)(t)},e.encode=function(t,e){return(!e||e<=0?i.XML:i.HTML)(t)},e.encodeXML=i.XML,e.encodeHTML4=e.encodeHTML5=e.encodeHTML=i.HTML,e.decodeXML=e.decodeXMLStrict=n.XML,e.decodeHTML4=e.decodeHTML5=e.decodeHTML=n.HTML,e.decodeHTML4Strict=e.decodeHTML5Strict=e.decodeHTMLStrict=n.HTMLStrict,e.escape=i.escape},194:(t,e,r)=>{var i=r(752),n=r(76),s=r(83),o=r(26),a=h(s),c=h(i);function h(t){var e=Object.keys(t).join("|"),r=p(t),i=new RegExp("&(?:"+(e+="|#[xX][\\da-fA-F]+|#\\d+")+");","g");return function(t){return String(t).replace(i,r)}}var u=function(){for(var t=Object.keys(n).sort(l),e=Object.keys(i).sort(l),r=0,s=0;r<e.length;r++)t[s]===e[r]?(e[r]+=";?",s++):e[r]+=";";var o=new RegExp("&(?:"+e.join("|")+"|#[xX][\\da-fA-F]+;?|#\\d+;?)","g"),a=p(i);function c(t){return";"!==t.substr(-1)&&(t+=";"),a(t)}return function(t){return String(t).replace(o,c)}}();function l(t,e){return t<e?1:-1}function p(t){return function(e){return"#"===e.charAt(1)?"X"===e.charAt(2)||"x"===e.charAt(2)?o(parseInt(e.substr(3),16)):o(parseInt(e.substr(2),10)):t[e.slice(1,-1)]}}t.exports={XML:a,HTML:u,HTMLStrict:c}},26:(t,e,r)=>{var i=r(549);t.exports=function(t){if(t>=55296&&t<=57343||t>1114111)return"�";t in i&&(t=i[t]);var e="";return t>65535&&(t-=65536,e+=String.fromCharCode(t>>>10&1023|55296),t=56320|1023&t),e+String.fromCharCode(t)}},322:(t,e,r)=>{var i=a(r(83)),n=c(i);e.XML=f(i,n);var s=a(r(752)),o=c(s);function a(t){return Object.keys(t).sort().reduce((function(e,r){return e[t[r]]="&"+r+";",e}),{})}function c(t){var e=[],r=[];return Object.keys(t).forEach((function(t){1===t.length?e.push("\\"+t):r.push(t)})),r.unshift("["+e.join("")+"]"),new RegExp(r.join("|"),"g")}e.HTML=f(s,o);var h=/[^\0-\x7F]/g,u=/[\uD800-\uDBFF][\uDC00-\uDFFF]/g;function l(t){return"&#x"+t.charCodeAt(0).toString(16).toUpperCase()+";"}function p(t){return"&#x"+(1024*(t.charCodeAt(0)-55296)+t.charCodeAt(1)-56320+65536).toString(16).toUpperCase()+";"}function f(t,e){function r(e){return t[e]}return function(t){return t.replace(e,r).replace(u,p).replace(h,l)}}var d=c(i);e.escape=function(t){return t.replace(d,l).replace(u,p).replace(h,l)}},549:t=>{"use strict";t.exports=JSON.parse('{"0":65533,"128":8364,"130":8218,"131":402,"132":8222,"133":8230,"134":8224,"135":8225,"136":710,"137":8240,"138":352,"139":8249,"140":338,"142":381,"145":8216,"146":8217,"147":8220,"148":8221,"149":8226,"150":8211,"151":8212,"152":732,"153":8482,"154":353,"155":8250,"156":339,"158":382,"159":376}')},752:t=>{"use strict";t.exports=JSON.parse('{"Aacute":"Á","aacute":"á","Abreve":"Ă","abreve":"ă","ac":"∾","acd":"∿","acE":"∾̳","Acirc":"Â","acirc":"â","acute":"´","Acy":"А","acy":"а","AElig":"Æ","aelig":"æ","af":"⁡","Afr":"𝔄","afr":"𝔞","Agrave":"À","agrave":"à","alefsym":"ℵ","aleph":"ℵ","Alpha":"Α","alpha":"α","Amacr":"Ā","amacr":"ā","amalg":"⨿","amp":"&","AMP":"&","andand":"⩕","And":"⩓","and":"∧","andd":"⩜","andslope":"⩘","andv":"⩚","ang":"∠","ange":"⦤","angle":"∠","angmsdaa":"⦨","angmsdab":"⦩","angmsdac":"⦪","angmsdad":"⦫","angmsdae":"⦬","angmsdaf":"⦭","angmsdag":"⦮","angmsdah":"⦯","angmsd":"∡","angrt":"∟","angrtvb":"⊾","angrtvbd":"⦝","angsph":"∢","angst":"Å","angzarr":"⍼","Aogon":"Ą","aogon":"ą","Aopf":"𝔸","aopf":"𝕒","apacir":"⩯","ap":"≈","apE":"⩰","ape":"≊","apid":"≋","apos":"\'","ApplyFunction":"⁡","approx":"≈","approxeq":"≊","Aring":"Å","aring":"å","Ascr":"𝒜","ascr":"𝒶","Assign":"≔","ast":"*","asymp":"≈","asympeq":"≍","Atilde":"Ã","atilde":"ã","Auml":"Ä","auml":"ä","awconint":"∳","awint":"⨑","backcong":"≌","backepsilon":"϶","backprime":"‵","backsim":"∽","backsimeq":"⋍","Backslash":"∖","Barv":"⫧","barvee":"⊽","barwed":"⌅","Barwed":"⌆","barwedge":"⌅","bbrk":"⎵","bbrktbrk":"⎶","bcong":"≌","Bcy":"Б","bcy":"б","bdquo":"„","becaus":"∵","because":"∵","Because":"∵","bemptyv":"⦰","bepsi":"϶","bernou":"ℬ","Bernoullis":"ℬ","Beta":"Β","beta":"β","beth":"ℶ","between":"≬","Bfr":"𝔅","bfr":"𝔟","bigcap":"⋂","bigcirc":"◯","bigcup":"⋃","bigodot":"⨀","bigoplus":"⨁","bigotimes":"⨂","bigsqcup":"⨆","bigstar":"★","bigtriangledown":"▽","bigtriangleup":"△","biguplus":"⨄","bigvee":"⋁","bigwedge":"⋀","bkarow":"⤍","blacklozenge":"⧫","blacksquare":"▪","blacktriangle":"▴","blacktriangledown":"▾","blacktriangleleft":"◂","blacktriangleright":"▸","blank":"␣","blk12":"▒","blk14":"░","blk34":"▓","block":"█","bne":"=⃥","bnequiv":"≡⃥","bNot":"⫭","bnot":"⌐","Bopf":"𝔹","bopf":"𝕓","bot":"⊥","bottom":"⊥","bowtie":"⋈","boxbox":"⧉","boxdl":"┐","boxdL":"╕","boxDl":"╖","boxDL":"╗","boxdr":"┌","boxdR":"╒","boxDr":"╓","boxDR":"╔","boxh":"─","boxH":"═","boxhd":"┬","boxHd":"╤","boxhD":"╥","boxHD":"╦","boxhu":"┴","boxHu":"╧","boxhU":"╨","boxHU":"╩","boxminus":"⊟","boxplus":"⊞","boxtimes":"⊠","boxul":"┘","boxuL":"╛","boxUl":"╜","boxUL":"╝","boxur":"└","boxuR":"╘","boxUr":"╙","boxUR":"╚","boxv":"│","boxV":"║","boxvh":"┼","boxvH":"╪","boxVh":"╫","boxVH":"╬","boxvl":"┤","boxvL":"╡","boxVl":"╢","boxVL":"╣","boxvr":"├","boxvR":"╞","boxVr":"╟","boxVR":"╠","bprime":"‵","breve":"˘","Breve":"˘","brvbar":"¦","bscr":"𝒷","Bscr":"ℬ","bsemi":"⁏","bsim":"∽","bsime":"⋍","bsolb":"⧅","bsol":"\\\\","bsolhsub":"⟈","bull":"•","bullet":"•","bump":"≎","bumpE":"⪮","bumpe":"≏","Bumpeq":"≎","bumpeq":"≏","Cacute":"Ć","cacute":"ć","capand":"⩄","capbrcup":"⩉","capcap":"⩋","cap":"∩","Cap":"⋒","capcup":"⩇","capdot":"⩀","CapitalDifferentialD":"ⅅ","caps":"∩︀","caret":"⁁","caron":"ˇ","Cayleys":"ℭ","ccaps":"⩍","Ccaron":"Č","ccaron":"č","Ccedil":"Ç","ccedil":"ç","Ccirc":"Ĉ","ccirc":"ĉ","Cconint":"∰","ccups":"⩌","ccupssm":"⩐","Cdot":"Ċ","cdot":"ċ","cedil":"¸","Cedilla":"¸","cemptyv":"⦲","cent":"¢","centerdot":"·","CenterDot":"·","cfr":"𝔠","Cfr":"ℭ","CHcy":"Ч","chcy":"ч","check":"✓","checkmark":"✓","Chi":"Χ","chi":"χ","circ":"ˆ","circeq":"≗","circlearrowleft":"↺","circlearrowright":"↻","circledast":"⊛","circledcirc":"⊚","circleddash":"⊝","CircleDot":"⊙","circledR":"®","circledS":"Ⓢ","CircleMinus":"⊖","CirclePlus":"⊕","CircleTimes":"⊗","cir":"○","cirE":"⧃","cire":"≗","cirfnint":"⨐","cirmid":"⫯","cirscir":"⧂","ClockwiseContourIntegral":"∲","CloseCurlyDoubleQuote":"”","CloseCurlyQuote":"’","clubs":"♣","clubsuit":"♣","colon":":","Colon":"∷","Colone":"⩴","colone":"≔","coloneq":"≔","comma":",","commat":"@","comp":"∁","compfn":"∘","complement":"∁","complexes":"ℂ","cong":"≅","congdot":"⩭","Congruent":"≡","conint":"∮","Conint":"∯","ContourIntegral":"∮","copf":"𝕔","Copf":"ℂ","coprod":"∐","Coproduct":"∐","copy":"©","COPY":"©","copysr":"℗","CounterClockwiseContourIntegral":"∳","crarr":"↵","cross":"✗","Cross":"⨯","Cscr":"𝒞","cscr":"𝒸","csub":"⫏","csube":"⫑","csup":"⫐","csupe":"⫒","ctdot":"⋯","cudarrl":"⤸","cudarrr":"⤵","cuepr":"⋞","cuesc":"⋟","cularr":"↶","cularrp":"⤽","cupbrcap":"⩈","cupcap":"⩆","CupCap":"≍","cup":"∪","Cup":"⋓","cupcup":"⩊","cupdot":"⊍","cupor":"⩅","cups":"∪︀","curarr":"↷","curarrm":"⤼","curlyeqprec":"⋞","curlyeqsucc":"⋟","curlyvee":"⋎","curlywedge":"⋏","curren":"¤","curvearrowleft":"↶","curvearrowright":"↷","cuvee":"⋎","cuwed":"⋏","cwconint":"∲","cwint":"∱","cylcty":"⌭","dagger":"†","Dagger":"‡","daleth":"ℸ","darr":"↓","Darr":"↡","dArr":"⇓","dash":"‐","Dashv":"⫤","dashv":"⊣","dbkarow":"⤏","dblac":"˝","Dcaron":"Ď","dcaron":"ď","Dcy":"Д","dcy":"д","ddagger":"‡","ddarr":"⇊","DD":"ⅅ","dd":"ⅆ","DDotrahd":"⤑","ddotseq":"⩷","deg":"°","Del":"∇","Delta":"Δ","delta":"δ","demptyv":"⦱","dfisht":"⥿","Dfr":"𝔇","dfr":"𝔡","dHar":"⥥","dharl":"⇃","dharr":"⇂","DiacriticalAcute":"´","DiacriticalDot":"˙","DiacriticalDoubleAcute":"˝","DiacriticalGrave":"`","DiacriticalTilde":"˜","diam":"⋄","diamond":"⋄","Diamond":"⋄","diamondsuit":"♦","diams":"♦","die":"¨","DifferentialD":"ⅆ","digamma":"ϝ","disin":"⋲","div":"÷","divide":"÷","divideontimes":"⋇","divonx":"⋇","DJcy":"Ђ","djcy":"ђ","dlcorn":"⌞","dlcrop":"⌍","dollar":"$","Dopf":"𝔻","dopf":"𝕕","Dot":"¨","dot":"˙","DotDot":"⃜","doteq":"≐","doteqdot":"≑","DotEqual":"≐","dotminus":"∸","dotplus":"∔","dotsquare":"⊡","doublebarwedge":"⌆","DoubleContourIntegral":"∯","DoubleDot":"¨","DoubleDownArrow":"⇓","DoubleLeftArrow":"⇐","DoubleLeftRightArrow":"⇔","DoubleLeftTee":"⫤","DoubleLongLeftArrow":"⟸","DoubleLongLeftRightArrow":"⟺","DoubleLongRightArrow":"⟹","DoubleRightArrow":"⇒","DoubleRightTee":"⊨","DoubleUpArrow":"⇑","DoubleUpDownArrow":"⇕","DoubleVerticalBar":"∥","DownArrowBar":"⤓","downarrow":"↓","DownArrow":"↓","Downarrow":"⇓","DownArrowUpArrow":"⇵","DownBreve":"̑","downdownarrows":"⇊","downharpoonleft":"⇃","downharpoonright":"⇂","DownLeftRightVector":"⥐","DownLeftTeeVector":"⥞","DownLeftVectorBar":"⥖","DownLeftVector":"↽","DownRightTeeVector":"⥟","DownRightVectorBar":"⥗","DownRightVector":"⇁","DownTeeArrow":"↧","DownTee":"⊤","drbkarow":"⤐","drcorn":"⌟","drcrop":"⌌","Dscr":"𝒟","dscr":"𝒹","DScy":"Ѕ","dscy":"ѕ","dsol":"⧶","Dstrok":"Đ","dstrok":"đ","dtdot":"⋱","dtri":"▿","dtrif":"▾","duarr":"⇵","duhar":"⥯","dwangle":"⦦","DZcy":"Џ","dzcy":"џ","dzigrarr":"⟿","Eacute":"É","eacute":"é","easter":"⩮","Ecaron":"Ě","ecaron":"ě","Ecirc":"Ê","ecirc":"ê","ecir":"≖","ecolon":"≕","Ecy":"Э","ecy":"э","eDDot":"⩷","Edot":"Ė","edot":"ė","eDot":"≑","ee":"ⅇ","efDot":"≒","Efr":"𝔈","efr":"𝔢","eg":"⪚","Egrave":"È","egrave":"è","egs":"⪖","egsdot":"⪘","el":"⪙","Element":"∈","elinters":"⏧","ell":"ℓ","els":"⪕","elsdot":"⪗","Emacr":"Ē","emacr":"ē","empty":"∅","emptyset":"∅","EmptySmallSquare":"◻","emptyv":"∅","EmptyVerySmallSquare":"▫","emsp13":" ","emsp14":" ","emsp":" ","ENG":"Ŋ","eng":"ŋ","ensp":" ","Eogon":"Ę","eogon":"ę","Eopf":"𝔼","eopf":"𝕖","epar":"⋕","eparsl":"⧣","eplus":"⩱","epsi":"ε","Epsilon":"Ε","epsilon":"ε","epsiv":"ϵ","eqcirc":"≖","eqcolon":"≕","eqsim":"≂","eqslantgtr":"⪖","eqslantless":"⪕","Equal":"⩵","equals":"=","EqualTilde":"≂","equest":"≟","Equilibrium":"⇌","equiv":"≡","equivDD":"⩸","eqvparsl":"⧥","erarr":"⥱","erDot":"≓","escr":"ℯ","Escr":"ℰ","esdot":"≐","Esim":"⩳","esim":"≂","Eta":"Η","eta":"η","ETH":"Ð","eth":"ð","Euml":"Ë","euml":"ë","euro":"€","excl":"!","exist":"∃","Exists":"∃","expectation":"ℰ","exponentiale":"ⅇ","ExponentialE":"ⅇ","fallingdotseq":"≒","Fcy":"Ф","fcy":"ф","female":"♀","ffilig":"ﬃ","fflig":"ﬀ","ffllig":"ﬄ","Ffr":"𝔉","ffr":"𝔣","filig":"ﬁ","FilledSmallSquare":"◼","FilledVerySmallSquare":"▪","fjlig":"fj","flat":"♭","fllig":"ﬂ","fltns":"▱","fnof":"ƒ","Fopf":"𝔽","fopf":"𝕗","forall":"∀","ForAll":"∀","fork":"⋔","forkv":"⫙","Fouriertrf":"ℱ","fpartint":"⨍","frac12":"½","frac13":"⅓","frac14":"¼","frac15":"⅕","frac16":"⅙","frac18":"⅛","frac23":"⅔","frac25":"⅖","frac34":"¾","frac35":"⅗","frac38":"⅜","frac45":"⅘","frac56":"⅚","frac58":"⅝","frac78":"⅞","frasl":"⁄","frown":"⌢","fscr":"𝒻","Fscr":"ℱ","gacute":"ǵ","Gamma":"Γ","gamma":"γ","Gammad":"Ϝ","gammad":"ϝ","gap":"⪆","Gbreve":"Ğ","gbreve":"ğ","Gcedil":"Ģ","Gcirc":"Ĝ","gcirc":"ĝ","Gcy":"Г","gcy":"г","Gdot":"Ġ","gdot":"ġ","ge":"≥","gE":"≧","gEl":"⪌","gel":"⋛","geq":"≥","geqq":"≧","geqslant":"⩾","gescc":"⪩","ges":"⩾","gesdot":"⪀","gesdoto":"⪂","gesdotol":"⪄","gesl":"⋛︀","gesles":"⪔","Gfr":"𝔊","gfr":"𝔤","gg":"≫","Gg":"⋙","ggg":"⋙","gimel":"ℷ","GJcy":"Ѓ","gjcy":"ѓ","gla":"⪥","gl":"≷","glE":"⪒","glj":"⪤","gnap":"⪊","gnapprox":"⪊","gne":"⪈","gnE":"≩","gneq":"⪈","gneqq":"≩","gnsim":"⋧","Gopf":"𝔾","gopf":"𝕘","grave":"`","GreaterEqual":"≥","GreaterEqualLess":"⋛","GreaterFullEqual":"≧","GreaterGreater":"⪢","GreaterLess":"≷","GreaterSlantEqual":"⩾","GreaterTilde":"≳","Gscr":"𝒢","gscr":"ℊ","gsim":"≳","gsime":"⪎","gsiml":"⪐","gtcc":"⪧","gtcir":"⩺","gt":">","GT":">","Gt":"≫","gtdot":"⋗","gtlPar":"⦕","gtquest":"⩼","gtrapprox":"⪆","gtrarr":"⥸","gtrdot":"⋗","gtreqless":"⋛","gtreqqless":"⪌","gtrless":"≷","gtrsim":"≳","gvertneqq":"≩︀","gvnE":"≩︀","Hacek":"ˇ","hairsp":" ","half":"½","hamilt":"ℋ","HARDcy":"Ъ","hardcy":"ъ","harrcir":"⥈","harr":"↔","hArr":"⇔","harrw":"↭","Hat":"^","hbar":"ℏ","Hcirc":"Ĥ","hcirc":"ĥ","hearts":"♥","heartsuit":"♥","hellip":"…","hercon":"⊹","hfr":"𝔥","Hfr":"ℌ","HilbertSpace":"ℋ","hksearow":"⤥","hkswarow":"⤦","hoarr":"⇿","homtht":"∻","hookleftarrow":"↩","hookrightarrow":"↪","hopf":"𝕙","Hopf":"ℍ","horbar":"―","HorizontalLine":"─","hscr":"𝒽","Hscr":"ℋ","hslash":"ℏ","Hstrok":"Ħ","hstrok":"ħ","HumpDownHump":"≎","HumpEqual":"≏","hybull":"⁃","hyphen":"‐","Iacute":"Í","iacute":"í","ic":"⁣","Icirc":"Î","icirc":"î","Icy":"И","icy":"и","Idot":"İ","IEcy":"Е","iecy":"е","iexcl":"¡","iff":"⇔","ifr":"𝔦","Ifr":"ℑ","Igrave":"Ì","igrave":"ì","ii":"ⅈ","iiiint":"⨌","iiint":"∭","iinfin":"⧜","iiota":"℩","IJlig":"Ĳ","ijlig":"ĳ","Imacr":"Ī","imacr":"ī","image":"ℑ","ImaginaryI":"ⅈ","imagline":"ℐ","imagpart":"ℑ","imath":"ı","Im":"ℑ","imof":"⊷","imped":"Ƶ","Implies":"⇒","incare":"℅","in":"∈","infin":"∞","infintie":"⧝","inodot":"ı","intcal":"⊺","int":"∫","Int":"∬","integers":"ℤ","Integral":"∫","intercal":"⊺","Intersection":"⋂","intlarhk":"⨗","intprod":"⨼","InvisibleComma":"⁣","InvisibleTimes":"⁢","IOcy":"Ё","iocy":"ё","Iogon":"Į","iogon":"į","Iopf":"𝕀","iopf":"𝕚","Iota":"Ι","iota":"ι","iprod":"⨼","iquest":"¿","iscr":"𝒾","Iscr":"ℐ","isin":"∈","isindot":"⋵","isinE":"⋹","isins":"⋴","isinsv":"⋳","isinv":"∈","it":"⁢","Itilde":"Ĩ","itilde":"ĩ","Iukcy":"І","iukcy":"і","Iuml":"Ï","iuml":"ï","Jcirc":"Ĵ","jcirc":"ĵ","Jcy":"Й","jcy":"й","Jfr":"𝔍","jfr":"𝔧","jmath":"ȷ","Jopf":"𝕁","jopf":"𝕛","Jscr":"𝒥","jscr":"𝒿","Jsercy":"Ј","jsercy":"ј","Jukcy":"Є","jukcy":"є","Kappa":"Κ","kappa":"κ","kappav":"ϰ","Kcedil":"Ķ","kcedil":"ķ","Kcy":"К","kcy":"к","Kfr":"𝔎","kfr":"𝔨","kgreen":"ĸ","KHcy":"Х","khcy":"х","KJcy":"Ќ","kjcy":"ќ","Kopf":"𝕂","kopf":"𝕜","Kscr":"𝒦","kscr":"𝓀","lAarr":"⇚","Lacute":"Ĺ","lacute":"ĺ","laemptyv":"⦴","lagran":"ℒ","Lambda":"Λ","lambda":"λ","lang":"⟨","Lang":"⟪","langd":"⦑","langle":"⟨","lap":"⪅","Laplacetrf":"ℒ","laquo":"«","larrb":"⇤","larrbfs":"⤟","larr":"←","Larr":"↞","lArr":"⇐","larrfs":"⤝","larrhk":"↩","larrlp":"↫","larrpl":"⤹","larrsim":"⥳","larrtl":"↢","latail":"⤙","lAtail":"⤛","lat":"⪫","late":"⪭","lates":"⪭︀","lbarr":"⤌","lBarr":"⤎","lbbrk":"❲","lbrace":"{","lbrack":"[","lbrke":"⦋","lbrksld":"⦏","lbrkslu":"⦍","Lcaron":"Ľ","lcaron":"ľ","Lcedil":"Ļ","lcedil":"ļ","lceil":"⌈","lcub":"{","Lcy":"Л","lcy":"л","ldca":"⤶","ldquo":"“","ldquor":"„","ldrdhar":"⥧","ldrushar":"⥋","ldsh":"↲","le":"≤","lE":"≦","LeftAngleBracket":"⟨","LeftArrowBar":"⇤","leftarrow":"←","LeftArrow":"←","Leftarrow":"⇐","LeftArrowRightArrow":"⇆","leftarrowtail":"↢","LeftCeiling":"⌈","LeftDoubleBracket":"⟦","LeftDownTeeVector":"⥡","LeftDownVectorBar":"⥙","LeftDownVector":"⇃","LeftFloor":"⌊","leftharpoondown":"↽","leftharpoonup":"↼","leftleftarrows":"⇇","leftrightarrow":"↔","LeftRightArrow":"↔","Leftrightarrow":"⇔","leftrightarrows":"⇆","leftrightharpoons":"⇋","leftrightsquigarrow":"↭","LeftRightVector":"⥎","LeftTeeArrow":"↤","LeftTee":"⊣","LeftTeeVector":"⥚","leftthreetimes":"⋋","LeftTriangleBar":"⧏","LeftTriangle":"⊲","LeftTriangleEqual":"⊴","LeftUpDownVector":"⥑","LeftUpTeeVector":"⥠","LeftUpVectorBar":"⥘","LeftUpVector":"↿","LeftVectorBar":"⥒","LeftVector":"↼","lEg":"⪋","leg":"⋚","leq":"≤","leqq":"≦","leqslant":"⩽","lescc":"⪨","les":"⩽","lesdot":"⩿","lesdoto":"⪁","lesdotor":"⪃","lesg":"⋚︀","lesges":"⪓","lessapprox":"⪅","lessdot":"⋖","lesseqgtr":"⋚","lesseqqgtr":"⪋","LessEqualGreater":"⋚","LessFullEqual":"≦","LessGreater":"≶","lessgtr":"≶","LessLess":"⪡","lesssim":"≲","LessSlantEqual":"⩽","LessTilde":"≲","lfisht":"⥼","lfloor":"⌊","Lfr":"𝔏","lfr":"𝔩","lg":"≶","lgE":"⪑","lHar":"⥢","lhard":"↽","lharu":"↼","lharul":"⥪","lhblk":"▄","LJcy":"Љ","ljcy":"љ","llarr":"⇇","ll":"≪","Ll":"⋘","llcorner":"⌞","Lleftarrow":"⇚","llhard":"⥫","lltri":"◺","Lmidot":"Ŀ","lmidot":"ŀ","lmoustache":"⎰","lmoust":"⎰","lnap":"⪉","lnapprox":"⪉","lne":"⪇","lnE":"≨","lneq":"⪇","lneqq":"≨","lnsim":"⋦","loang":"⟬","loarr":"⇽","lobrk":"⟦","longleftarrow":"⟵","LongLeftArrow":"⟵","Longleftarrow":"⟸","longleftrightarrow":"⟷","LongLeftRightArrow":"⟷","Longleftrightarrow":"⟺","longmapsto":"⟼","longrightarrow":"⟶","LongRightArrow":"⟶","Longrightarrow":"⟹","looparrowleft":"↫","looparrowright":"↬","lopar":"⦅","Lopf":"𝕃","lopf":"𝕝","loplus":"⨭","lotimes":"⨴","lowast":"∗","lowbar":"_","LowerLeftArrow":"↙","LowerRightArrow":"↘","loz":"◊","lozenge":"◊","lozf":"⧫","lpar":"(","lparlt":"⦓","lrarr":"⇆","lrcorner":"⌟","lrhar":"⇋","lrhard":"⥭","lrm":"‎","lrtri":"⊿","lsaquo":"‹","lscr":"𝓁","Lscr":"ℒ","lsh":"↰","Lsh":"↰","lsim":"≲","lsime":"⪍","lsimg":"⪏","lsqb":"[","lsquo":"‘","lsquor":"‚","Lstrok":"Ł","lstrok":"ł","ltcc":"⪦","ltcir":"⩹","lt":"<","LT":"<","Lt":"≪","ltdot":"⋖","lthree":"⋋","ltimes":"⋉","ltlarr":"⥶","ltquest":"⩻","ltri":"◃","ltrie":"⊴","ltrif":"◂","ltrPar":"⦖","lurdshar":"⥊","luruhar":"⥦","lvertneqq":"≨︀","lvnE":"≨︀","macr":"¯","male":"♂","malt":"✠","maltese":"✠","Map":"⤅","map":"↦","mapsto":"↦","mapstodown":"↧","mapstoleft":"↤","mapstoup":"↥","marker":"▮","mcomma":"⨩","Mcy":"М","mcy":"м","mdash":"—","mDDot":"∺","measuredangle":"∡","MediumSpace":" ","Mellintrf":"ℳ","Mfr":"𝔐","mfr":"𝔪","mho":"℧","micro":"µ","midast":"*","midcir":"⫰","mid":"∣","middot":"·","minusb":"⊟","minus":"−","minusd":"∸","minusdu":"⨪","MinusPlus":"∓","mlcp":"⫛","mldr":"…","mnplus":"∓","models":"⊧","Mopf":"𝕄","mopf":"𝕞","mp":"∓","mscr":"𝓂","Mscr":"ℳ","mstpos":"∾","Mu":"Μ","mu":"μ","multimap":"⊸","mumap":"⊸","nabla":"∇","Nacute":"Ń","nacute":"ń","nang":"∠⃒","nap":"≉","napE":"⩰̸","napid":"≋̸","napos":"ŉ","napprox":"≉","natural":"♮","naturals":"ℕ","natur":"♮","nbsp":" ","nbump":"≎̸","nbumpe":"≏̸","ncap":"⩃","Ncaron":"Ň","ncaron":"ň","Ncedil":"Ņ","ncedil":"ņ","ncong":"≇","ncongdot":"⩭̸","ncup":"⩂","Ncy":"Н","ncy":"н","ndash":"–","nearhk":"⤤","nearr":"↗","neArr":"⇗","nearrow":"↗","ne":"≠","nedot":"≐̸","NegativeMediumSpace":"​","NegativeThickSpace":"​","NegativeThinSpace":"​","NegativeVeryThinSpace":"​","nequiv":"≢","nesear":"⤨","nesim":"≂̸","NestedGreaterGreater":"≫","NestedLessLess":"≪","NewLine":"\\n","nexist":"∄","nexists":"∄","Nfr":"𝔑","nfr":"𝔫","ngE":"≧̸","nge":"≱","ngeq":"≱","ngeqq":"≧̸","ngeqslant":"⩾̸","nges":"⩾̸","nGg":"⋙̸","ngsim":"≵","nGt":"≫⃒","ngt":"≯","ngtr":"≯","nGtv":"≫̸","nharr":"↮","nhArr":"⇎","nhpar":"⫲","ni":"∋","nis":"⋼","nisd":"⋺","niv":"∋","NJcy":"Њ","njcy":"њ","nlarr":"↚","nlArr":"⇍","nldr":"‥","nlE":"≦̸","nle":"≰","nleftarrow":"↚","nLeftarrow":"⇍","nleftrightarrow":"↮","nLeftrightarrow":"⇎","nleq":"≰","nleqq":"≦̸","nleqslant":"⩽̸","nles":"⩽̸","nless":"≮","nLl":"⋘̸","nlsim":"≴","nLt":"≪⃒","nlt":"≮","nltri":"⋪","nltrie":"⋬","nLtv":"≪̸","nmid":"∤","NoBreak":"⁠","NonBreakingSpace":" ","nopf":"𝕟","Nopf":"ℕ","Not":"⫬","not":"¬","NotCongruent":"≢","NotCupCap":"≭","NotDoubleVerticalBar":"∦","NotElement":"∉","NotEqual":"≠","NotEqualTilde":"≂̸","NotExists":"∄","NotGreater":"≯","NotGreaterEqual":"≱","NotGreaterFullEqual":"≧̸","NotGreaterGreater":"≫̸","NotGreaterLess":"≹","NotGreaterSlantEqual":"⩾̸","NotGreaterTilde":"≵","NotHumpDownHump":"≎̸","NotHumpEqual":"≏̸","notin":"∉","notindot":"⋵̸","notinE":"⋹̸","notinva":"∉","notinvb":"⋷","notinvc":"⋶","NotLeftTriangleBar":"⧏̸","NotLeftTriangle":"⋪","NotLeftTriangleEqual":"⋬","NotLess":"≮","NotLessEqual":"≰","NotLessGreater":"≸","NotLessLess":"≪̸","NotLessSlantEqual":"⩽̸","NotLessTilde":"≴","NotNestedGreaterGreater":"⪢̸","NotNestedLessLess":"⪡̸","notni":"∌","notniva":"∌","notnivb":"⋾","notnivc":"⋽","NotPrecedes":"⊀","NotPrecedesEqual":"⪯̸","NotPrecedesSlantEqual":"⋠","NotReverseElement":"∌","NotRightTriangleBar":"⧐̸","NotRightTriangle":"⋫","NotRightTriangleEqual":"⋭","NotSquareSubset":"⊏̸","NotSquareSubsetEqual":"⋢","NotSquareSuperset":"⊐̸","NotSquareSupersetEqual":"⋣","NotSubset":"⊂⃒","NotSubsetEqual":"⊈","NotSucceeds":"⊁","NotSucceedsEqual":"⪰̸","NotSucceedsSlantEqual":"⋡","NotSucceedsTilde":"≿̸","NotSuperset":"⊃⃒","NotSupersetEqual":"⊉","NotTilde":"≁","NotTildeEqual":"≄","NotTildeFullEqual":"≇","NotTildeTilde":"≉","NotVerticalBar":"∤","nparallel":"∦","npar":"∦","nparsl":"⫽⃥","npart":"∂̸","npolint":"⨔","npr":"⊀","nprcue":"⋠","nprec":"⊀","npreceq":"⪯̸","npre":"⪯̸","nrarrc":"⤳̸","nrarr":"↛","nrArr":"⇏","nrarrw":"↝̸","nrightarrow":"↛","nRightarrow":"⇏","nrtri":"⋫","nrtrie":"⋭","nsc":"⊁","nsccue":"⋡","nsce":"⪰̸","Nscr":"𝒩","nscr":"𝓃","nshortmid":"∤","nshortparallel":"∦","nsim":"≁","nsime":"≄","nsimeq":"≄","nsmid":"∤","nspar":"∦","nsqsube":"⋢","nsqsupe":"⋣","nsub":"⊄","nsubE":"⫅̸","nsube":"⊈","nsubset":"⊂⃒","nsubseteq":"⊈","nsubseteqq":"⫅̸","nsucc":"⊁","nsucceq":"⪰̸","nsup":"⊅","nsupE":"⫆̸","nsupe":"⊉","nsupset":"⊃⃒","nsupseteq":"⊉","nsupseteqq":"⫆̸","ntgl":"≹","Ntilde":"Ñ","ntilde":"ñ","ntlg":"≸","ntriangleleft":"⋪","ntrianglelefteq":"⋬","ntriangleright":"⋫","ntrianglerighteq":"⋭","Nu":"Ν","nu":"ν","num":"#","numero":"№","numsp":" ","nvap":"≍⃒","nvdash":"⊬","nvDash":"⊭","nVdash":"⊮","nVDash":"⊯","nvge":"≥⃒","nvgt":">⃒","nvHarr":"⤄","nvinfin":"⧞","nvlArr":"⤂","nvle":"≤⃒","nvlt":"<⃒","nvltrie":"⊴⃒","nvrArr":"⤃","nvrtrie":"⊵⃒","nvsim":"∼⃒","nwarhk":"⤣","nwarr":"↖","nwArr":"⇖","nwarrow":"↖","nwnear":"⤧","Oacute":"Ó","oacute":"ó","oast":"⊛","Ocirc":"Ô","ocirc":"ô","ocir":"⊚","Ocy":"О","ocy":"о","odash":"⊝","Odblac":"Ő","odblac":"ő","odiv":"⨸","odot":"⊙","odsold":"⦼","OElig":"Œ","oelig":"œ","ofcir":"⦿","Ofr":"𝔒","ofr":"𝔬","ogon":"˛","Ograve":"Ò","ograve":"ò","ogt":"⧁","ohbar":"⦵","ohm":"Ω","oint":"∮","olarr":"↺","olcir":"⦾","olcross":"⦻","oline":"‾","olt":"⧀","Omacr":"Ō","omacr":"ō","Omega":"Ω","omega":"ω","Omicron":"Ο","omicron":"ο","omid":"⦶","ominus":"⊖","Oopf":"𝕆","oopf":"𝕠","opar":"⦷","OpenCurlyDoubleQuote":"“","OpenCurlyQuote":"‘","operp":"⦹","oplus":"⊕","orarr":"↻","Or":"⩔","or":"∨","ord":"⩝","order":"ℴ","orderof":"ℴ","ordf":"ª","ordm":"º","origof":"⊶","oror":"⩖","orslope":"⩗","orv":"⩛","oS":"Ⓢ","Oscr":"𝒪","oscr":"ℴ","Oslash":"Ø","oslash":"ø","osol":"⊘","Otilde":"Õ","otilde":"õ","otimesas":"⨶","Otimes":"⨷","otimes":"⊗","Ouml":"Ö","ouml":"ö","ovbar":"⌽","OverBar":"‾","OverBrace":"⏞","OverBracket":"⎴","OverParenthesis":"⏜","para":"¶","parallel":"∥","par":"∥","parsim":"⫳","parsl":"⫽","part":"∂","PartialD":"∂","Pcy":"П","pcy":"п","percnt":"%","period":".","permil":"‰","perp":"⊥","pertenk":"‱","Pfr":"𝔓","pfr":"𝔭","Phi":"Φ","phi":"φ","phiv":"ϕ","phmmat":"ℳ","phone":"☎","Pi":"Π","pi":"π","pitchfork":"⋔","piv":"ϖ","planck":"ℏ","planckh":"ℎ","plankv":"ℏ","plusacir":"⨣","plusb":"⊞","pluscir":"⨢","plus":"+","plusdo":"∔","plusdu":"⨥","pluse":"⩲","PlusMinus":"±","plusmn":"±","plussim":"⨦","plustwo":"⨧","pm":"±","Poincareplane":"ℌ","pointint":"⨕","popf":"𝕡","Popf":"ℙ","pound":"£","prap":"⪷","Pr":"⪻","pr":"≺","prcue":"≼","precapprox":"⪷","prec":"≺","preccurlyeq":"≼","Precedes":"≺","PrecedesEqual":"⪯","PrecedesSlantEqual":"≼","PrecedesTilde":"≾","preceq":"⪯","precnapprox":"⪹","precneqq":"⪵","precnsim":"⋨","pre":"⪯","prE":"⪳","precsim":"≾","prime":"′","Prime":"″","primes":"ℙ","prnap":"⪹","prnE":"⪵","prnsim":"⋨","prod":"∏","Product":"∏","profalar":"⌮","profline":"⌒","profsurf":"⌓","prop":"∝","Proportional":"∝","Proportion":"∷","propto":"∝","prsim":"≾","prurel":"⊰","Pscr":"𝒫","pscr":"𝓅","Psi":"Ψ","psi":"ψ","puncsp":" ","Qfr":"𝔔","qfr":"𝔮","qint":"⨌","qopf":"𝕢","Qopf":"ℚ","qprime":"⁗","Qscr":"𝒬","qscr":"𝓆","quaternions":"ℍ","quatint":"⨖","quest":"?","questeq":"≟","quot":"\\"","QUOT":"\\"","rAarr":"⇛","race":"∽̱","Racute":"Ŕ","racute":"ŕ","radic":"√","raemptyv":"⦳","rang":"⟩","Rang":"⟫","rangd":"⦒","range":"⦥","rangle":"⟩","raquo":"»","rarrap":"⥵","rarrb":"⇥","rarrbfs":"⤠","rarrc":"⤳","rarr":"→","Rarr":"↠","rArr":"⇒","rarrfs":"⤞","rarrhk":"↪","rarrlp":"↬","rarrpl":"⥅","rarrsim":"⥴","Rarrtl":"⤖","rarrtl":"↣","rarrw":"↝","ratail":"⤚","rAtail":"⤜","ratio":"∶","rationals":"ℚ","rbarr":"⤍","rBarr":"⤏","RBarr":"⤐","rbbrk":"❳","rbrace":"}","rbrack":"]","rbrke":"⦌","rbrksld":"⦎","rbrkslu":"⦐","Rcaron":"Ř","rcaron":"ř","Rcedil":"Ŗ","rcedil":"ŗ","rceil":"⌉","rcub":"}","Rcy":"Р","rcy":"р","rdca":"⤷","rdldhar":"⥩","rdquo":"”","rdquor":"”","rdsh":"↳","real":"ℜ","realine":"ℛ","realpart":"ℜ","reals":"ℝ","Re":"ℜ","rect":"▭","reg":"®","REG":"®","ReverseElement":"∋","ReverseEquilibrium":"⇋","ReverseUpEquilibrium":"⥯","rfisht":"⥽","rfloor":"⌋","rfr":"𝔯","Rfr":"ℜ","rHar":"⥤","rhard":"⇁","rharu":"⇀","rharul":"⥬","Rho":"Ρ","rho":"ρ","rhov":"ϱ","RightAngleBracket":"⟩","RightArrowBar":"⇥","rightarrow":"→","RightArrow":"→","Rightarrow":"⇒","RightArrowLeftArrow":"⇄","rightarrowtail":"↣","RightCeiling":"⌉","RightDoubleBracket":"⟧","RightDownTeeVector":"⥝","RightDownVectorBar":"⥕","RightDownVector":"⇂","RightFloor":"⌋","rightharpoondown":"⇁","rightharpoonup":"⇀","rightleftarrows":"⇄","rightleftharpoons":"⇌","rightrightarrows":"⇉","rightsquigarrow":"↝","RightTeeArrow":"↦","RightTee":"⊢","RightTeeVector":"⥛","rightthreetimes":"⋌","RightTriangleBar":"⧐","RightTriangle":"⊳","RightTriangleEqual":"⊵","RightUpDownVector":"⥏","RightUpTeeVector":"⥜","RightUpVectorBar":"⥔","RightUpVector":"↾","RightVectorBar":"⥓","RightVector":"⇀","ring":"˚","risingdotseq":"≓","rlarr":"⇄","rlhar":"⇌","rlm":"‏","rmoustache":"⎱","rmoust":"⎱","rnmid":"⫮","roang":"⟭","roarr":"⇾","robrk":"⟧","ropar":"⦆","ropf":"𝕣","Ropf":"ℝ","roplus":"⨮","rotimes":"⨵","RoundImplies":"⥰","rpar":")","rpargt":"⦔","rppolint":"⨒","rrarr":"⇉","Rrightarrow":"⇛","rsaquo":"›","rscr":"𝓇","Rscr":"ℛ","rsh":"↱","Rsh":"↱","rsqb":"]","rsquo":"’","rsquor":"’","rthree":"⋌","rtimes":"⋊","rtri":"▹","rtrie":"⊵","rtrif":"▸","rtriltri":"⧎","RuleDelayed":"⧴","ruluhar":"⥨","rx":"℞","Sacute":"Ś","sacute":"ś","sbquo":"‚","scap":"⪸","Scaron":"Š","scaron":"š","Sc":"⪼","sc":"≻","sccue":"≽","sce":"⪰","scE":"⪴","Scedil":"Ş","scedil":"ş","Scirc":"Ŝ","scirc":"ŝ","scnap":"⪺","scnE":"⪶","scnsim":"⋩","scpolint":"⨓","scsim":"≿","Scy":"С","scy":"с","sdotb":"⊡","sdot":"⋅","sdote":"⩦","searhk":"⤥","searr":"↘","seArr":"⇘","searrow":"↘","sect":"§","semi":";","seswar":"⤩","setminus":"∖","setmn":"∖","sext":"✶","Sfr":"𝔖","sfr":"𝔰","sfrown":"⌢","sharp":"♯","SHCHcy":"Щ","shchcy":"щ","SHcy":"Ш","shcy":"ш","ShortDownArrow":"↓","ShortLeftArrow":"←","shortmid":"∣","shortparallel":"∥","ShortRightArrow":"→","ShortUpArrow":"↑","shy":"­","Sigma":"Σ","sigma":"σ","sigmaf":"ς","sigmav":"ς","sim":"∼","simdot":"⩪","sime":"≃","simeq":"≃","simg":"⪞","simgE":"⪠","siml":"⪝","simlE":"⪟","simne":"≆","simplus":"⨤","simrarr":"⥲","slarr":"←","SmallCircle":"∘","smallsetminus":"∖","smashp":"⨳","smeparsl":"⧤","smid":"∣","smile":"⌣","smt":"⪪","smte":"⪬","smtes":"⪬︀","SOFTcy":"Ь","softcy":"ь","solbar":"⌿","solb":"⧄","sol":"/","Sopf":"𝕊","sopf":"𝕤","spades":"♠","spadesuit":"♠","spar":"∥","sqcap":"⊓","sqcaps":"⊓︀","sqcup":"⊔","sqcups":"⊔︀","Sqrt":"√","sqsub":"⊏","sqsube":"⊑","sqsubset":"⊏","sqsubseteq":"⊑","sqsup":"⊐","sqsupe":"⊒","sqsupset":"⊐","sqsupseteq":"⊒","square":"□","Square":"□","SquareIntersection":"⊓","SquareSubset":"⊏","SquareSubsetEqual":"⊑","SquareSuperset":"⊐","SquareSupersetEqual":"⊒","SquareUnion":"⊔","squarf":"▪","squ":"□","squf":"▪","srarr":"→","Sscr":"𝒮","sscr":"𝓈","ssetmn":"∖","ssmile":"⌣","sstarf":"⋆","Star":"⋆","star":"☆","starf":"★","straightepsilon":"ϵ","straightphi":"ϕ","strns":"¯","sub":"⊂","Sub":"⋐","subdot":"⪽","subE":"⫅","sube":"⊆","subedot":"⫃","submult":"⫁","subnE":"⫋","subne":"⊊","subplus":"⪿","subrarr":"⥹","subset":"⊂","Subset":"⋐","subseteq":"⊆","subseteqq":"⫅","SubsetEqual":"⊆","subsetneq":"⊊","subsetneqq":"⫋","subsim":"⫇","subsub":"⫕","subsup":"⫓","succapprox":"⪸","succ":"≻","succcurlyeq":"≽","Succeeds":"≻","SucceedsEqual":"⪰","SucceedsSlantEqual":"≽","SucceedsTilde":"≿","succeq":"⪰","succnapprox":"⪺","succneqq":"⪶","succnsim":"⋩","succsim":"≿","SuchThat":"∋","sum":"∑","Sum":"∑","sung":"♪","sup1":"¹","sup2":"²","sup3":"³","sup":"⊃","Sup":"⋑","supdot":"⪾","supdsub":"⫘","supE":"⫆","supe":"⊇","supedot":"⫄","Superset":"⊃","SupersetEqual":"⊇","suphsol":"⟉","suphsub":"⫗","suplarr":"⥻","supmult":"⫂","supnE":"⫌","supne":"⊋","supplus":"⫀","supset":"⊃","Supset":"⋑","supseteq":"⊇","supseteqq":"⫆","supsetneq":"⊋","supsetneqq":"⫌","supsim":"⫈","supsub":"⫔","supsup":"⫖","swarhk":"⤦","swarr":"↙","swArr":"⇙","swarrow":"↙","swnwar":"⤪","szlig":"ß","Tab":"\\t","target":"⌖","Tau":"Τ","tau":"τ","tbrk":"⎴","Tcaron":"Ť","tcaron":"ť","Tcedil":"Ţ","tcedil":"ţ","Tcy":"Т","tcy":"т","tdot":"⃛","telrec":"⌕","Tfr":"𝔗","tfr":"𝔱","there4":"∴","therefore":"∴","Therefore":"∴","Theta":"Θ","theta":"θ","thetasym":"ϑ","thetav":"ϑ","thickapprox":"≈","thicksim":"∼","ThickSpace":"  ","ThinSpace":" ","thinsp":" ","thkap":"≈","thksim":"∼","THORN":"Þ","thorn":"þ","tilde":"˜","Tilde":"∼","TildeEqual":"≃","TildeFullEqual":"≅","TildeTilde":"≈","timesbar":"⨱","timesb":"⊠","times":"×","timesd":"⨰","tint":"∭","toea":"⤨","topbot":"⌶","topcir":"⫱","top":"⊤","Topf":"𝕋","topf":"𝕥","topfork":"⫚","tosa":"⤩","tprime":"‴","trade":"™","TRADE":"™","triangle":"▵","triangledown":"▿","triangleleft":"◃","trianglelefteq":"⊴","triangleq":"≜","triangleright":"▹","trianglerighteq":"⊵","tridot":"◬","trie":"≜","triminus":"⨺","TripleDot":"⃛","triplus":"⨹","trisb":"⧍","tritime":"⨻","trpezium":"⏢","Tscr":"𝒯","tscr":"𝓉","TScy":"Ц","tscy":"ц","TSHcy":"Ћ","tshcy":"ћ","Tstrok":"Ŧ","tstrok":"ŧ","twixt":"≬","twoheadleftarrow":"↞","twoheadrightarrow":"↠","Uacute":"Ú","uacute":"ú","uarr":"↑","Uarr":"↟","uArr":"⇑","Uarrocir":"⥉","Ubrcy":"Ў","ubrcy":"ў","Ubreve":"Ŭ","ubreve":"ŭ","Ucirc":"Û","ucirc":"û","Ucy":"У","ucy":"у","udarr":"⇅","Udblac":"Ű","udblac":"ű","udhar":"⥮","ufisht":"⥾","Ufr":"𝔘","ufr":"𝔲","Ugrave":"Ù","ugrave":"ù","uHar":"⥣","uharl":"↿","uharr":"↾","uhblk":"▀","ulcorn":"⌜","ulcorner":"⌜","ulcrop":"⌏","ultri":"◸","Umacr":"Ū","umacr":"ū","uml":"¨","UnderBar":"_","UnderBrace":"⏟","UnderBracket":"⎵","UnderParenthesis":"⏝","Union":"⋃","UnionPlus":"⊎","Uogon":"Ų","uogon":"ų","Uopf":"𝕌","uopf":"𝕦","UpArrowBar":"⤒","uparrow":"↑","UpArrow":"↑","Uparrow":"⇑","UpArrowDownArrow":"⇅","updownarrow":"↕","UpDownArrow":"↕","Updownarrow":"⇕","UpEquilibrium":"⥮","upharpoonleft":"↿","upharpoonright":"↾","uplus":"⊎","UpperLeftArrow":"↖","UpperRightArrow":"↗","upsi":"υ","Upsi":"ϒ","upsih":"ϒ","Upsilon":"Υ","upsilon":"υ","UpTeeArrow":"↥","UpTee":"⊥","upuparrows":"⇈","urcorn":"⌝","urcorner":"⌝","urcrop":"⌎","Uring":"Ů","uring":"ů","urtri":"◹","Uscr":"𝒰","uscr":"𝓊","utdot":"⋰","Utilde":"Ũ","utilde":"ũ","utri":"▵","utrif":"▴","uuarr":"⇈","Uuml":"Ü","uuml":"ü","uwangle":"⦧","vangrt":"⦜","varepsilon":"ϵ","varkappa":"ϰ","varnothing":"∅","varphi":"ϕ","varpi":"ϖ","varpropto":"∝","varr":"↕","vArr":"⇕","varrho":"ϱ","varsigma":"ς","varsubsetneq":"⊊︀","varsubsetneqq":"⫋︀","varsupsetneq":"⊋︀","varsupsetneqq":"⫌︀","vartheta":"ϑ","vartriangleleft":"⊲","vartriangleright":"⊳","vBar":"⫨","Vbar":"⫫","vBarv":"⫩","Vcy":"В","vcy":"в","vdash":"⊢","vDash":"⊨","Vdash":"⊩","VDash":"⊫","Vdashl":"⫦","veebar":"⊻","vee":"∨","Vee":"⋁","veeeq":"≚","vellip":"⋮","verbar":"|","Verbar":"‖","vert":"|","Vert":"‖","VerticalBar":"∣","VerticalLine":"|","VerticalSeparator":"❘","VerticalTilde":"≀","VeryThinSpace":" ","Vfr":"𝔙","vfr":"𝔳","vltri":"⊲","vnsub":"⊂⃒","vnsup":"⊃⃒","Vopf":"𝕍","vopf":"𝕧","vprop":"∝","vrtri":"⊳","Vscr":"𝒱","vscr":"𝓋","vsubnE":"⫋︀","vsubne":"⊊︀","vsupnE":"⫌︀","vsupne":"⊋︀","Vvdash":"⊪","vzigzag":"⦚","Wcirc":"Ŵ","wcirc":"ŵ","wedbar":"⩟","wedge":"∧","Wedge":"⋀","wedgeq":"≙","weierp":"℘","Wfr":"𝔚","wfr":"𝔴","Wopf":"𝕎","wopf":"𝕨","wp":"℘","wr":"≀","wreath":"≀","Wscr":"𝒲","wscr":"𝓌","xcap":"⋂","xcirc":"◯","xcup":"⋃","xdtri":"▽","Xfr":"𝔛","xfr":"𝔵","xharr":"⟷","xhArr":"⟺","Xi":"Ξ","xi":"ξ","xlarr":"⟵","xlArr":"⟸","xmap":"⟼","xnis":"⋻","xodot":"⨀","Xopf":"𝕏","xopf":"𝕩","xoplus":"⨁","xotime":"⨂","xrarr":"⟶","xrArr":"⟹","Xscr":"𝒳","xscr":"𝓍","xsqcup":"⨆","xuplus":"⨄","xutri":"△","xvee":"⋁","xwedge":"⋀","Yacute":"Ý","yacute":"ý","YAcy":"Я","yacy":"я","Ycirc":"Ŷ","ycirc":"ŷ","Ycy":"Ы","ycy":"ы","yen":"¥","Yfr":"𝔜","yfr":"𝔶","YIcy":"Ї","yicy":"ї","Yopf":"𝕐","yopf":"𝕪","Yscr":"𝒴","yscr":"𝓎","YUcy":"Ю","yucy":"ю","yuml":"ÿ","Yuml":"Ÿ","Zacute":"Ź","zacute":"ź","Zcaron":"Ž","zcaron":"ž","Zcy":"З","zcy":"з","Zdot":"Ż","zdot":"ż","zeetrf":"ℨ","ZeroWidthSpace":"​","Zeta":"Ζ","zeta":"ζ","zfr":"𝔷","Zfr":"ℨ","ZHcy":"Ж","zhcy":"ж","zigrarr":"⇝","zopf":"𝕫","Zopf":"ℤ","Zscr":"𝒵","zscr":"𝓏","zwj":"‍","zwnj":"‌"}')},76:t=>{"use strict";t.exports=JSON.parse('{"Aacute":"Á","aacute":"á","Acirc":"Â","acirc":"â","acute":"´","AElig":"Æ","aelig":"æ","Agrave":"À","agrave":"à","amp":"&","AMP":"&","Aring":"Å","aring":"å","Atilde":"Ã","atilde":"ã","Auml":"Ä","auml":"ä","brvbar":"¦","Ccedil":"Ç","ccedil":"ç","cedil":"¸","cent":"¢","copy":"©","COPY":"©","curren":"¤","deg":"°","divide":"÷","Eacute":"É","eacute":"é","Ecirc":"Ê","ecirc":"ê","Egrave":"È","egrave":"è","ETH":"Ð","eth":"ð","Euml":"Ë","euml":"ë","frac12":"½","frac14":"¼","frac34":"¾","gt":">","GT":">","Iacute":"Í","iacute":"í","Icirc":"Î","icirc":"î","iexcl":"¡","Igrave":"Ì","igrave":"ì","iquest":"¿","Iuml":"Ï","iuml":"ï","laquo":"«","lt":"<","LT":"<","macr":"¯","micro":"µ","middot":"·","nbsp":" ","not":"¬","Ntilde":"Ñ","ntilde":"ñ","Oacute":"Ó","oacute":"ó","Ocirc":"Ô","ocirc":"ô","Ograve":"Ò","ograve":"ò","ordf":"ª","ordm":"º","Oslash":"Ø","oslash":"ø","Otilde":"Õ","otilde":"õ","Ouml":"Ö","ouml":"ö","para":"¶","plusmn":"±","pound":"£","quot":"\\"","QUOT":"\\"","raquo":"»","reg":"®","REG":"®","sect":"§","shy":"­","sup1":"¹","sup2":"²","sup3":"³","szlig":"ß","THORN":"Þ","thorn":"þ","times":"×","Uacute":"Ú","uacute":"ú","Ucirc":"Û","ucirc":"û","Ugrave":"Ù","ugrave":"ù","uml":"¨","Uuml":"Ü","uuml":"ü","Yacute":"Ý","yacute":"ý","yen":"¥","yuml":"ÿ"}')},83:t=>{"use strict";t.exports=JSON.parse('{"amp":"&","apos":"\'","gt":">","lt":"<","quot":"\\""}')},187:t=>{"use strict";var e,r="object"==typeof Reflect?Reflect:null,i=r&&"function"==typeof r.apply?r.apply:function(t,e,r){return Function.prototype.apply.call(t,e,r)};e=r&&"function"==typeof r.ownKeys?r.ownKeys:Object.getOwnPropertySymbols?function(t){return Object.getOwnPropertyNames(t).concat(Object.getOwnPropertySymbols(t))}:function(t){return Object.getOwnPropertyNames(t)};var n=Number.isNaN||function(t){return t!=t};function s(){s.init.call(this)}t.exports=s,t.exports.once=function(t,e){return new Promise((function(r,i){function n(){void 0!==s&&t.removeListener("error",s),r([].slice.call(arguments))}var s;"error"!==e&&(s=function(r){t.removeListener(e,n),i(r)},t.once("error",s)),t.once(e,n)}))},s.EventEmitter=s,s.prototype._events=void 0,s.prototype._eventsCount=0,s.prototype._maxListeners=void 0;var o=10;function a(t){if("function"!=typeof t)throw new TypeError('The "listener" argument must be of type Function. Received type '+typeof t)}function c(t){return void 0===t._maxListeners?s.defaultMaxListeners:t._maxListeners}function h(t,e,r,i){var n,s,o,h;if(a(r),void 0===(s=t._events)?(s=t._events=Object.create(null),t._eventsCount=0):(void 0!==s.newListener&&(t.emit("newListener",e,r.listener?r.listener:r),s=t._events),o=s[e]),void 0===o)o=s[e]=r,++t._eventsCount;else if("function"==typeof o?o=s[e]=i?[r,o]:[o,r]:i?o.unshift(r):o.push(r),(n=c(t))>0&&o.length>n&&!o.warned){o.warned=!0;var u=new Error("Possible EventEmitter memory leak detected. "+o.length+" "+String(e)+" listeners added. Use emitter.setMaxListeners() to increase limit");u.name="MaxListenersExceededWarning",u.emitter=t,u.type=e,u.count=o.length,h=u,console&&console.warn&&console.warn(h)}return t}function u(){if(!this.fired)return this.target.removeListener(this.type,this.wrapFn),this.fired=!0,0===arguments.length?this.listener.call(this.target):this.listener.apply(this.target,arguments)}function l(t,e,r){var i={fired:!1,wrapFn:void 0,target:t,type:e,listener:r},n=u.bind(i);return n.listener=r,i.wrapFn=n,n}function p(t,e,r){var i=t._events;if(void 0===i)return[];var n=i[e];return void 0===n?[]:"function"==typeof n?r?[n.listener||n]:[n]:r?function(t){for(var e=new Array(t.length),r=0;r<e.length;++r)e[r]=t[r].listener||t[r];return e}(n):d(n,n.length)}function f(t){var e=this._events;if(void 0!==e){var r=e[t];if("function"==typeof r)return 1;if(void 0!==r)return r.length}return 0}function d(t,e){for(var r=new Array(e),i=0;i<e;++i)r[i]=t[i];return r}Object.defineProperty(s,"defaultMaxListeners",{enumerable:!0,get:function(){return o},set:function(t){if("number"!=typeof t||t<0||n(t))throw new RangeError('The value of "defaultMaxListeners" is out of range. It must be a non-negative number. Received '+t+".");o=t}}),s.init=function(){void 0!==this._events&&this._events!==Object.getPrototypeOf(this)._events||(this._events=Object.create(null),this._eventsCount=0),this._maxListeners=this._maxListeners||void 0},s.prototype.setMaxListeners=function(t){if("number"!=typeof t||t<0||n(t))throw new RangeError('The value of "n" is out of range. It must be a non-negative number. Received '+t+".");return this._maxListeners=t,this},s.prototype.getMaxListeners=function(){return c(this)},s.prototype.emit=function(t){for(var e=[],r=1;r<arguments.length;r++)e.push(arguments[r]);var n="error"===t,s=this._events;if(void 0!==s)n=n&&void 0===s.error;else if(!n)return!1;if(n){var o;if(e.length>0&&(o=e[0]),o instanceof Error)throw o;var a=new Error("Unhandled error."+(o?" ("+o.message+")":""));throw a.context=o,a}var c=s[t];if(void 0===c)return!1;if("function"==typeof c)i(c,this,e);else{var h=c.length,u=d(c,h);for(r=0;r<h;++r)i(u[r],this,e)}return!0},s.prototype.addListener=function(t,e){return h(this,t,e,!1)},s.prototype.on=s.prototype.addListener,s.prototype.prependListener=function(t,e){return h(this,t,e,!0)},s.prototype.once=function(t,e){return a(e),this.on(t,l(this,t,e)),this},s.prototype.prependOnceListener=function(t,e){return a(e),this.prependListener(t,l(this,t,e)),this},s.prototype.removeListener=function(t,e){var r,i,n,s,o;if(a(e),void 0===(i=this._events))return this;if(void 0===(r=i[t]))return this;if(r===e||r.listener===e)0==--this._eventsCount?this._events=Object.create(null):(delete i[t],i.removeListener&&this.emit("removeListener",t,r.listener||e));else if("function"!=typeof r){for(n=-1,s=r.length-1;s>=0;s--)if(r[s]===e||r[s].listener===e){o=r[s].listener,n=s;break}if(n<0)return this;0===n?r.shift():function(t,e){for(;e+1<t.length;e++)t[e]=t[e+1];t.pop()}(r,n),1===r.length&&(i[t]=r[0]),void 0!==i.removeListener&&this.emit("removeListener",t,o||e)}return this},s.prototype.off=s.prototype.removeListener,s.prototype.removeAllListeners=function(t){var e,r,i;if(void 0===(r=this._events))return this;if(void 0===r.removeListener)return 0===arguments.length?(this._events=Object.create(null),this._eventsCount=0):void 0!==r[t]&&(0==--this._eventsCount?this._events=Object.create(null):delete r[t]),this;if(0===arguments.length){var n,s=Object.keys(r);for(i=0;i<s.length;++i)"removeListener"!==(n=s[i])&&this.removeAllListeners(n);return this.removeAllListeners("removeListener"),this._events=Object.create(null),this._eventsCount=0,this}if("function"==typeof(e=r[t]))this.removeListener(t,e);else if(void 0!==e)for(i=e.length-1;i>=0;i--)this.removeListener(t,e[i]);return this},s.prototype.listeners=function(t){return p(this,t,!0)},s.prototype.rawListeners=function(t){return p(this,t,!1)},s.listenerCount=function(t,e){return"function"==typeof t.listenerCount?t.listenerCount(e):f.call(t,e)},s.prototype.listenerCount=f,s.prototype.eventNames=function(){return this._eventsCount>0?e(this._events):[]}},449:(t,e,r)=>{function i(t){this._cbs=t||{},this.events=[]}t.exports=i;var n=r(719).EVENTS;Object.keys(n).forEach((function(t){if(0===n[t])t="on"+t,i.prototype[t]=function(){this.events.push([t]),this._cbs[t]&&this._cbs[t]()};else if(1===n[t])t="on"+t,i.prototype[t]=function(e){this.events.push([t,e]),this._cbs[t]&&this._cbs[t](e)};else{if(2!==n[t])throw Error("wrong number of arguments");t="on"+t,i.prototype[t]=function(e,r){this.events.push([t,e,r]),this._cbs[t]&&this._cbs[t](e,r)}}})),i.prototype.onreset=function(){this.events=[],this._cbs.onreset&&this._cbs.onreset()},i.prototype.restart=function(){this._cbs.onreset&&this._cbs.onreset();for(var t=0,e=this.events.length;t<e;t++)if(this._cbs[this.events[t][0]]){var r=this.events[t].length;1===r?this._cbs[this.events[t][0]]():2===r?this._cbs[this.events[t][0]](this.events[t][1]):this._cbs[this.events[t][0]](this.events[t][1],this.events[t][2])}}},870:(t,e,r)=>{var i=r(753),n=r(417);function s(t,e){this.init(t,e)}function o(t,e){return n.getElementsByTagName(t,e,!0)}function a(t,e){return n.getElementsByTagName(t,e,!0,1)[0]}function c(t,e,r){return n.getText(n.getElementsByTagName(t,e,r,1)).trim()}function h(t,e,r,i,n){var s=c(r,i,n);s&&(t[e]=s)}r(717)(s,i),s.prototype.init=i;var u=function(t){return"rss"===t||"feed"===t||"rdf:RDF"===t};s.prototype.onend=function(){var t,e,r={},n=a(u,this.dom);n&&("feed"===n.name?(e=n.children,r.type="atom",h(r,"id","id",e),h(r,"title","title",e),(t=a("link",e))&&(t=t.attribs)&&(t=t.href)&&(r.link=t),h(r,"description","subtitle",e),(t=c("updated",e))&&(r.updated=new Date(t)),h(r,"author","email",e,!0),r.items=o("entry",e).map((function(t){var e,r={};return h(r,"id","id",t=t.children),h(r,"title","title",t),(e=a("link",t))&&(e=e.attribs)&&(e=e.href)&&(r.link=e),(e=c("summary",t)||c("content",t))&&(r.description=e),(e=c("updated",t))&&(r.pubDate=new Date(e)),r}))):(e=a("channel",n.children).children,r.type=n.name.substr(0,3),r.id="",h(r,"title","title",e),h(r,"link","link",e),h(r,"description","description",e),(t=c("lastBuildDate",e))&&(r.updated=new Date(t)),h(r,"author","managingEditor",e,!0),r.items=o("item",n.children).map((function(t){var e,r={};return h(r,"id","guid",t=t.children),h(r,"title","title",t),h(r,"link","link",t),h(r,"description","description",t),(e=c("pubDate",t))&&(r.pubDate=new Date(e)),r})))),this.dom=r,i.prototype._handleCallback.call(this,n?null:Error("couldn't find root of feed"))},t.exports=s},763:(t,e,r)=>{var i=r(889),n={input:!0,option:!0,optgroup:!0,select:!0,button:!0,datalist:!0,textarea:!0},s={tr:{tr:!0,th:!0,td:!0},th:{th:!0},td:{thead:!0,th:!0,td:!0},body:{head:!0,link:!0,script:!0},li:{li:!0},p:{p:!0},h1:{p:!0},h2:{p:!0},h3:{p:!0},h4:{p:!0},h5:{p:!0},h6:{p:!0},select:n,input:n,output:n,button:n,datalist:n,textarea:n,option:{option:!0},optgroup:{optgroup:!0}},o={__proto__:null,area:!0,base:!0,basefont:!0,br:!0,col:!0,command:!0,embed:!0,frame:!0,hr:!0,img:!0,input:!0,isindex:!0,keygen:!0,link:!0,meta:!0,param:!0,source:!0,track:!0,wbr:!0},a={__proto__:null,math:!0,svg:!0},c={__proto__:null,mi:!0,mo:!0,mn:!0,ms:!0,mtext:!0,"annotation-xml":!0,foreignObject:!0,desc:!0,title:!0},h=/\s|\//;function u(t,e){this._options=e||{},this._cbs=t||{},this._tagname="",this._attribname="",this._attribvalue="",this._attribs=null,this._stack=[],this._foreignContext=[],this.startIndex=0,this.endIndex=null,this._lowerCaseTagNames="lowerCaseTags"in this._options?!!this._options.lowerCaseTags:!this._options.xmlMode,this._lowerCaseAttributeNames="lowerCaseAttributeNames"in this._options?!!this._options.lowerCaseAttributeNames:!this._options.xmlMode,this._options.Tokenizer&&(i=this._options.Tokenizer),this._tokenizer=new i(this._options,this),this._cbs.onparserinit&&this._cbs.onparserinit(this)}r(717)(u,r(187).EventEmitter),u.prototype._updatePosition=function(t){null===this.endIndex?this._tokenizer._sectionStart<=t?this.startIndex=0:this.startIndex=this._tokenizer._sectionStart-t:this.startIndex=this.endIndex+1,this.endIndex=this._tokenizer.getAbsoluteIndex()},u.prototype.ontext=function(t){this._updatePosition(1),this.endIndex--,this._cbs.ontext&&this._cbs.ontext(t)},u.prototype.onopentagname=function(t){if(this._lowerCaseTagNames&&(t=t.toLowerCase()),this._tagname=t,!this._options.xmlMode&&t in s)for(var e;(e=this._stack[this._stack.length-1])in s[t];this.onclosetag(e));!this._options.xmlMode&&t in o||(this._stack.push(t),t in a?this._foreignContext.push(!0):t in c&&this._foreignContext.push(!1)),this._cbs.onopentagname&&this._cbs.onopentagname(t),this._cbs.onopentag&&(this._attribs={})},u.prototype.onopentagend=function(){this._updatePosition(1),this._attribs&&(this._cbs.onopentag&&this._cbs.onopentag(this._tagname,this._attribs),this._attribs=null),!this._options.xmlMode&&this._cbs.onclosetag&&this._tagname in o&&this._cbs.onclosetag(this._tagname),this._tagname=""},u.prototype.onclosetag=function(t){if(this._updatePosition(1),this._lowerCaseTagNames&&(t=t.toLowerCase()),(t in a||t in c)&&this._foreignContext.pop(),!this._stack.length||t in o&&!this._options.xmlMode)this._options.xmlMode||"br"!==t&&"p"!==t||(this.onopentagname(t),this._closeCurrentTag());else{var e=this._stack.lastIndexOf(t);if(-1!==e)if(this._cbs.onclosetag)for(e=this._stack.length-e;e--;)this._cbs.onclosetag(this._stack.pop());else this._stack.length=e;else"p"!==t||this._options.xmlMode||(this.onopentagname(t),this._closeCurrentTag())}},u.prototype.onselfclosingtag=function(){this._options.xmlMode||this._options.recognizeSelfClosing||this._foreignContext[this._foreignContext.length-1]?this._closeCurrentTag():this.onopentagend()},u.prototype._closeCurrentTag=function(){var t=this._tagname;this.onopentagend(),this._stack[this._stack.length-1]===t&&(this._cbs.onclosetag&&this._cbs.onclosetag(t),this._stack.pop())},u.prototype.onattribname=function(t){this._lowerCaseAttributeNames&&(t=t.toLowerCase()),this._attribname=t},u.prototype.onattribdata=function(t){this._attribvalue+=t},u.prototype.onattribend=function(){this._cbs.onattribute&&this._cbs.onattribute(this._attribname,this._attribvalue),this._attribs&&!Object.prototype.hasOwnProperty.call(this._attribs,this._attribname)&&(this._attribs[this._attribname]=this._attribvalue),this._attribname="",this._attribvalue=""},u.prototype._getInstructionName=function(t){var e=t.search(h),r=e<0?t:t.substr(0,e);return this._lowerCaseTagNames&&(r=r.toLowerCase()),r},u.prototype.ondeclaration=function(t){if(this._cbs.onprocessinginstruction){var e=this._getInstructionName(t);this._cbs.onprocessinginstruction("!"+e,"!"+t)}},u.prototype.onprocessinginstruction=function(t){if(this._cbs.onprocessinginstruction){var e=this._getInstructionName(t);this._cbs.onprocessinginstruction("?"+e,"?"+t)}},u.prototype.oncomment=function(t){this._updatePosition(4),this._cbs.oncomment&&this._cbs.oncomment(t),this._cbs.oncommentend&&this._cbs.oncommentend()},u.prototype.oncdata=function(t){this._updatePosition(1),this._options.xmlMode||this._options.recognizeCDATA?(this._cbs.oncdatastart&&this._cbs.oncdatastart(),this._cbs.ontext&&this._cbs.ontext(t),this._cbs.oncdataend&&this._cbs.oncdataend()):this.oncomment("[CDATA["+t+"]]")},u.prototype.onerror=function(t){this._cbs.onerror&&this._cbs.onerror(t)},u.prototype.onend=function(){if(this._cbs.onclosetag)for(var t=this._stack.length;t>0;this._cbs.onclosetag(this._stack[--t]));this._cbs.onend&&this._cbs.onend()},u.prototype.reset=function(){this._cbs.onreset&&this._cbs.onreset(),this._tokenizer.reset(),this._tagname="",this._attribname="",this._attribs=null,this._stack=[],this._cbs.onparserinit&&this._cbs.onparserinit(this)},u.prototype.parseComplete=function(t){this.reset(),this.end(t)},u.prototype.write=function(t){this._tokenizer.write(t)},u.prototype.end=function(t){this._tokenizer.end(t)},u.prototype.pause=function(){this._tokenizer.pause()},u.prototype.resume=function(){this._tokenizer.resume()},u.prototype.parseChunk=u.prototype.write,u.prototype.done=u.prototype.end,t.exports=u},321:(t,e,r)=>{function i(t){this._cbs=t||{}}t.exports=i;var n=r(719).EVENTS;Object.keys(n).forEach((function(t){if(0===n[t])t="on"+t,i.prototype[t]=function(){this._cbs[t]&&this._cbs[t]()};else if(1===n[t])t="on"+t,i.prototype[t]=function(e){this._cbs[t]&&this._cbs[t](e)};else{if(2!==n[t])throw Error("wrong number of arguments");t="on"+t,i.prototype[t]=function(e,r){this._cbs[t]&&this._cbs[t](e,r)}}}))},924:(t,e,r)=>{t.exports=n;var i=r(621);function n(t){i.call(this,new s(this),t)}function s(t){this.scope=t}r(717)(n,i),n.prototype.readable=!0;var o=r(719).EVENTS;Object.keys(o).forEach((function(t){if(0===o[t])s.prototype["on"+t]=function(){this.scope.emit(t)};else if(1===o[t])s.prototype["on"+t]=function(e){this.scope.emit(t,e)};else{if(2!==o[t])throw Error("wrong number of arguments!");s.prototype["on"+t]=function(e,r){this.scope.emit(t,e,r)}}}))},889:(t,e,r)=>{t.exports=_t;var i=r(26),n=r(752),s=r(76),o=r(83),a=0,c=a++,h=a++,u=a++,l=a++,p=a++,f=a++,d=a++,g=a++,_=a++,m=a++,b=a++,y=a++,v=a++,w=a++,x=a++,S=a++,E=a++,A=a++,T=a++,L=a++,q=a++,C=a++,k=a++,N=a++,D=a++,B=a++,R=a++,O=a++,I=a++,P=a++,U=a++,M=a++,V=a++,j=a++,H=a++,Y=a++,z=a++,F=a++,G=a++,X=a++,J=a++,Q=a++,W=a++,Z=a++,K=a++,$=a++,tt=a++,et=a++,rt=a++,it=a++,nt=a++,st=a++,ot=a++,at=a++,ct=a++,ht=0,ut=ht++,lt=ht++,pt=ht++;function ft(t){return" "===t||"\n"===t||"\t"===t||"\f"===t||"\r"===t}function dt(t,e,r){var i=t.toLowerCase();return t===i?function(t){t===i?this._state=e:(this._state=r,this._index--)}:function(n){n===i||n===t?this._state=e:(this._state=r,this._index--)}}function gt(t,e){var r=t.toLowerCase();return function(i){i===r||i===t?this._state=e:(this._state=u,this._index--)}}function _t(t,e){this._state=c,this._buffer="",this._sectionStart=0,this._index=0,this._bufferOffset=0,this._baseState=c,this._special=ut,this._cbs=e,this._running=!0,this._ended=!1,this._xmlMode=!(!t||!t.xmlMode),this._decodeEntities=!(!t||!t.decodeEntities)}_t.prototype._stateText=function(t){"<"===t?(this._index>this._sectionStart&&this._cbs.ontext(this._getSection()),this._state=h,this._sectionStart=this._index):this._decodeEntities&&this._special===ut&&"&"===t&&(this._index>this._sectionStart&&this._cbs.ontext(this._getSection()),this._baseState=c,this._state=nt,this._sectionStart=this._index)},_t.prototype._stateBeforeTagName=function(t){"/"===t?this._state=p:"<"===t?(this._cbs.ontext(this._getSection()),this._sectionStart=this._index):">"===t||this._special!==ut||ft(t)?this._state=c:"!"===t?(this._state=x,this._sectionStart=this._index+1):"?"===t?(this._state=E,this._sectionStart=this._index+1):(this._state=this._xmlMode||"s"!==t&&"S"!==t?u:U,this._sectionStart=this._index)},_t.prototype._stateInTagName=function(t){("/"===t||">"===t||ft(t))&&(this._emitToken("onopentagname"),this._state=g,this._index--)},_t.prototype._stateBeforeCloseingTagName=function(t){ft(t)||(">"===t?this._state=c:this._special!==ut?"s"===t||"S"===t?this._state=M:(this._state=c,this._index--):(this._state=f,this._sectionStart=this._index))},_t.prototype._stateInCloseingTagName=function(t){(">"===t||ft(t))&&(this._emitToken("onclosetag"),this._state=d,this._index--)},_t.prototype._stateAfterCloseingTagName=function(t){">"===t&&(this._state=c,this._sectionStart=this._index+1)},_t.prototype._stateBeforeAttributeName=function(t){">"===t?(this._cbs.onopentagend(),this._state=c,this._sectionStart=this._index+1):"/"===t?this._state=l:ft(t)||(this._state=_,this._sectionStart=this._index)},_t.prototype._stateInSelfClosingTag=function(t){">"===t?(this._cbs.onselfclosingtag(),this._state=c,this._sectionStart=this._index+1):ft(t)||(this._state=g,this._index--)},_t.prototype._stateInAttributeName=function(t){("="===t||"/"===t||">"===t||ft(t))&&(this._cbs.onattribname(this._getSection()),this._sectionStart=-1,this._state=m,this._index--)},_t.prototype._stateAfterAttributeName=function(t){"="===t?this._state=b:"/"===t||">"===t?(this._cbs.onattribend(),this._state=g,this._index--):ft(t)||(this._cbs.onattribend(),this._state=_,this._sectionStart=this._index)},_t.prototype._stateBeforeAttributeValue=function(t){'"'===t?(this._state=y,this._sectionStart=this._index+1):"'"===t?(this._state=v,this._sectionStart=this._index+1):ft(t)||(this._state=w,this._sectionStart=this._index,this._index--)},_t.prototype._stateInAttributeValueDoubleQuotes=function(t){'"'===t?(this._emitToken("onattribdata"),this._cbs.onattribend(),this._state=g):this._decodeEntities&&"&"===t&&(this._emitToken("onattribdata"),this._baseState=this._state,this._state=nt,this._sectionStart=this._index)},_t.prototype._stateInAttributeValueSingleQuotes=function(t){"'"===t?(this._emitToken("onattribdata"),this._cbs.onattribend(),this._state=g):this._decodeEntities&&"&"===t&&(this._emitToken("onattribdata"),this._baseState=this._state,this._state=nt,this._sectionStart=this._index)},_t.prototype._stateInAttributeValueNoQuotes=function(t){ft(t)||">"===t?(this._emitToken("onattribdata"),this._cbs.onattribend(),this._state=g,this._index--):this._decodeEntities&&"&"===t&&(this._emitToken("onattribdata"),this._baseState=this._state,this._state=nt,this._sectionStart=this._index)},_t.prototype._stateBeforeDeclaration=function(t){this._state="["===t?C:"-"===t?A:S},_t.prototype._stateInDeclaration=function(t){">"===t&&(this._cbs.ondeclaration(this._getSection()),this._state=c,this._sectionStart=this._index+1)},_t.prototype._stateInProcessingInstruction=function(t){">"===t&&(this._cbs.onprocessinginstruction(this._getSection()),this._state=c,this._sectionStart=this._index+1)},_t.prototype._stateBeforeComment=function(t){"-"===t?(this._state=T,this._sectionStart=this._index+1):this._state=S},_t.prototype._stateInComment=function(t){"-"===t&&(this._state=L)},_t.prototype._stateAfterComment1=function(t){this._state="-"===t?q:T},_t.prototype._stateAfterComment2=function(t){">"===t?(this._cbs.oncomment(this._buffer.substring(this._sectionStart,this._index-2)),this._state=c,this._sectionStart=this._index+1):"-"!==t&&(this._state=T)},_t.prototype._stateBeforeCdata1=dt("C",k,S),_t.prototype._stateBeforeCdata2=dt("D",N,S),_t.prototype._stateBeforeCdata3=dt("A",D,S),_t.prototype._stateBeforeCdata4=dt("T",B,S),_t.prototype._stateBeforeCdata5=dt("A",R,S),_t.prototype._stateBeforeCdata6=function(t){"["===t?(this._state=O,this._sectionStart=this._index+1):(this._state=S,this._index--)},_t.prototype._stateInCdata=function(t){"]"===t&&(this._state=I)},_t.prototype._stateAfterCdata1=function(t){this._state="]"===t?P:O},_t.prototype._stateAfterCdata2=function(t){">"===t?(this._cbs.oncdata(this._buffer.substring(this._sectionStart,this._index-2)),this._state=c,this._sectionStart=this._index+1):"]"!==t&&(this._state=O)},_t.prototype._stateBeforeSpecial=function(t){"c"===t||"C"===t?this._state=V:"t"===t||"T"===t?this._state=W:(this._state=u,this._index--)},_t.prototype._stateBeforeSpecialEnd=function(t){this._special!==lt||"c"!==t&&"C"!==t?this._special!==pt||"t"!==t&&"T"!==t?this._state=c:this._state=tt:this._state=F},_t.prototype._stateBeforeScript1=gt("R",j),_t.prototype._stateBeforeScript2=gt("I",H),_t.prototype._stateBeforeScript3=gt("P",Y),_t.prototype._stateBeforeScript4=gt("T",z),_t.prototype._stateBeforeScript5=function(t){("/"===t||">"===t||ft(t))&&(this._special=lt),this._state=u,this._index--},_t.prototype._stateAfterScript1=dt("R",G,c),_t.prototype._stateAfterScript2=dt("I",X,c),_t.prototype._stateAfterScript3=dt("P",J,c),_t.prototype._stateAfterScript4=dt("T",Q,c),_t.prototype._stateAfterScript5=function(t){">"===t||ft(t)?(this._special=ut,this._state=f,this._sectionStart=this._index-6,this._index--):this._state=c},_t.prototype._stateBeforeStyle1=gt("Y",Z),_t.prototype._stateBeforeStyle2=gt("L",K),_t.prototype._stateBeforeStyle3=gt("E",$),_t.prototype._stateBeforeStyle4=function(t){("/"===t||">"===t||ft(t))&&(this._special=pt),this._state=u,this._index--},_t.prototype._stateAfterStyle1=dt("Y",et,c),_t.prototype._stateAfterStyle2=dt("L",rt,c),_t.prototype._stateAfterStyle3=dt("E",it,c),_t.prototype._stateAfterStyle4=function(t){">"===t||ft(t)?(this._special=ut,this._state=f,this._sectionStart=this._index-5,this._index--):this._state=c},_t.prototype._stateBeforeEntity=dt("#",st,ot),_t.prototype._stateBeforeNumericEntity=dt("X",ct,at),_t.prototype._parseNamedEntityStrict=function(){if(this._sectionStart+1<this._index){var t=this._buffer.substring(this._sectionStart+1,this._index),e=this._xmlMode?o:n;e.hasOwnProperty(t)&&(this._emitPartial(e[t]),this._sectionStart=this._index+1)}},_t.prototype._parseLegacyEntity=function(){var t=this._sectionStart+1,e=this._index-t;for(e>6&&(e=6);e>=2;){var r=this._buffer.substr(t,e);if(s.hasOwnProperty(r))return this._emitPartial(s[r]),void(this._sectionStart+=e+1);e--}},_t.prototype._stateInNamedEntity=function(t){";"===t?(this._parseNamedEntityStrict(),this._sectionStart+1<this._index&&!this._xmlMode&&this._parseLegacyEntity(),this._state=this._baseState):(t<"a"||t>"z")&&(t<"A"||t>"Z")&&(t<"0"||t>"9")&&(this._xmlMode||this._sectionStart+1===this._index||(this._baseState!==c?"="!==t&&this._parseNamedEntityStrict():this._parseLegacyEntity()),this._state=this._baseState,this._index--)},_t.prototype._decodeNumericEntity=function(t,e){var r=this._sectionStart+t;if(r!==this._index){var n=this._buffer.substring(r,this._index),s=parseInt(n,e);this._emitPartial(i(s)),this._sectionStart=this._index}else this._sectionStart--;this._state=this._baseState},_t.prototype._stateInNumericEntity=function(t){";"===t?(this._decodeNumericEntity(2,10),this._sectionStart++):(t<"0"||t>"9")&&(this._xmlMode?this._state=this._baseState:this._decodeNumericEntity(2,10),this._index--)},_t.prototype._stateInHexEntity=function(t){";"===t?(this._decodeNumericEntity(3,16),this._sectionStart++):(t<"a"||t>"f")&&(t<"A"||t>"F")&&(t<"0"||t>"9")&&(this._xmlMode?this._state=this._baseState:this._decodeNumericEntity(3,16),this._index--)},_t.prototype._cleanup=function(){this._sectionStart<0?(this._buffer="",this._bufferOffset+=this._index,this._index=0):this._running&&(this._state===c?(this._sectionStart!==this._index&&this._cbs.ontext(this._buffer.substr(this._sectionStart)),this._buffer="",this._bufferOffset+=this._index,this._index=0):this._sectionStart===this._index?(this._buffer="",this._bufferOffset+=this._index,this._index=0):(this._buffer=this._buffer.substr(this._sectionStart),this._index-=this._sectionStart,this._bufferOffset+=this._sectionStart),this._sectionStart=0)},_t.prototype.write=function(t){this._ended&&this._cbs.onerror(Error(".write() after done!")),this._buffer+=t,this._parse()},_t.prototype._parse=function(){for(;this._index<this._buffer.length&&this._running;){var t=this._buffer.charAt(this._index);this._state===c?this._stateText(t):this._state===h?this._stateBeforeTagName(t):this._state===u?this._stateInTagName(t):this._state===p?this._stateBeforeCloseingTagName(t):this._state===f?this._stateInCloseingTagName(t):this._state===d?this._stateAfterCloseingTagName(t):this._state===l?this._stateInSelfClosingTag(t):this._state===g?this._stateBeforeAttributeName(t):this._state===_?this._stateInAttributeName(t):this._state===m?this._stateAfterAttributeName(t):this._state===b?this._stateBeforeAttributeValue(t):this._state===y?this._stateInAttributeValueDoubleQuotes(t):this._state===v?this._stateInAttributeValueSingleQuotes(t):this._state===w?this._stateInAttributeValueNoQuotes(t):this._state===x?this._stateBeforeDeclaration(t):this._state===S?this._stateInDeclaration(t):this._state===E?this._stateInProcessingInstruction(t):this._state===A?this._stateBeforeComment(t):this._state===T?this._stateInComment(t):this._state===L?this._stateAfterComment1(t):this._state===q?this._stateAfterComment2(t):this._state===C?this._stateBeforeCdata1(t):this._state===k?this._stateBeforeCdata2(t):this._state===N?this._stateBeforeCdata3(t):this._state===D?this._stateBeforeCdata4(t):this._state===B?this._stateBeforeCdata5(t):this._state===R?this._stateBeforeCdata6(t):this._state===O?this._stateInCdata(t):this._state===I?this._stateAfterCdata1(t):this._state===P?this._stateAfterCdata2(t):this._state===U?this._stateBeforeSpecial(t):this._state===M?this._stateBeforeSpecialEnd(t):this._state===V?this._stateBeforeScript1(t):this._state===j?this._stateBeforeScript2(t):this._state===H?this._stateBeforeScript3(t):this._state===Y?this._stateBeforeScript4(t):this._state===z?this._stateBeforeScript5(t):this._state===F?this._stateAfterScript1(t):this._state===G?this._stateAfterScript2(t):this._state===X?this._stateAfterScript3(t):this._state===J?this._stateAfterScript4(t):this._state===Q?this._stateAfterScript5(t):this._state===W?this._stateBeforeStyle1(t):this._state===Z?this._stateBeforeStyle2(t):this._state===K?this._stateBeforeStyle3(t):this._state===$?this._stateBeforeStyle4(t):this._state===tt?this._stateAfterStyle1(t):this._state===et?this._stateAfterStyle2(t):this._state===rt?this._stateAfterStyle3(t):this._state===it?this._stateAfterStyle4(t):this._state===nt?this._stateBeforeEntity(t):this._state===st?this._stateBeforeNumericEntity(t):this._state===ot?this._stateInNamedEntity(t):this._state===at?this._stateInNumericEntity(t):this._state===ct?this._stateInHexEntity(t):this._cbs.onerror(Error("unknown _state"),this._state),this._index++}this._cleanup()},_t.prototype.pause=function(){this._running=!1},_t.prototype.resume=function(){this._running=!0,this._index<this._buffer.length&&this._parse(),this._ended&&this._finish()},_t.prototype.end=function(t){this._ended&&this._cbs.onerror(Error(".end() after done!")),t&&this.write(t),this._ended=!0,this._running&&this._finish()},_t.prototype._finish=function(){this._sectionStart<this._index&&this._handleTrailingData(),this._cbs.onend()},_t.prototype._handleTrailingData=function(){var t=this._buffer.substr(this._sectionStart);this._state===O||this._state===I||this._state===P?this._cbs.oncdata(t):this._state===T||this._state===L||this._state===q?this._cbs.oncomment(t):this._state!==ot||this._xmlMode?this._state!==at||this._xmlMode?this._state!==ct||this._xmlMode?this._state!==u&&this._state!==g&&this._state!==b&&this._state!==m&&this._state!==_&&this._state!==v&&this._state!==y&&this._state!==w&&this._state!==f&&this._cbs.ontext(t):(this._decodeNumericEntity(3,16),this._sectionStart<this._index&&(this._state=this._baseState,this._handleTrailingData())):(this._decodeNumericEntity(2,10),this._sectionStart<this._index&&(this._state=this._baseState,this._handleTrailingData())):(this._parseLegacyEntity(),this._sectionStart<this._index&&(this._state=this._baseState,this._handleTrailingData()))},_t.prototype.reset=function(){_t.call(this,{xmlMode:this._xmlMode,decodeEntities:this._decodeEntities},this._cbs)},_t.prototype.getAbsoluteIndex=function(){return this._bufferOffset+this._index},_t.prototype._getSection=function(){return this._buffer.substring(this._sectionStart,this._index)},_t.prototype._emitToken=function(t){this._cbs[t](this._getSection()),this._sectionStart=-1},_t.prototype._emitPartial=function(t){this._baseState!==c?this._cbs.onattribdata(t):this._cbs.ontext(t)}},621:(t,e,r)=>{t.exports=a;var i=r(763),n=r(994).Writable,s=r(553).s,o=r(764).Buffer;function a(t,e){var r=this._parser=new i(t,e),o=this._decoder=new s;n.call(this,{decodeStrings:!1}),this.once("finish",(function(){r.end(o.end())}))}r(717)(a,n),a.prototype._write=function(t,e,r){t instanceof o&&(t=this._decoder.write(t)),this._parser.write(t),r()}},719:(t,e,r)=>{var i=r(763),n=r(753);function s(e,r){return delete t.exports[e],t.exports[e]=r,r}t.exports={Parser:i,Tokenizer:r(889),ElementType:r(431),DomHandler:n,get FeedHandler(){return s("FeedHandler",r(870))},get Stream(){return s("Stream",r(924))},get WritableStream(){return s("WritableStream",r(621))},get ProxyHandler(){return s("ProxyHandler",r(321))},get DomUtils(){return s("DomUtils",r(417))},get CollectingHandler(){return s("CollectingHandler",r(449))},DefaultHandler:n,get RssHandler(){return s("RssHandler",this.FeedHandler)},parseDOM:function(t,e){var r=new n(e);return new i(r,e).end(t),r.dom},parseFeed:function(e,r){var n=new t.exports.FeedHandler(r);return new i(n,r).end(e),n.dom},createDomStream:function(t,e,r){var s=new n(t,e,r);return new i(s,e)},EVENTS:{attribute:2,cdatastart:0,cdataend:0,text:1,processinginstruction:2,comment:1,commentend:0,closetag:1,opentag:2,opentagname:1,error:1,end:0}}},645:(t,e)=>{e.read=function(t,e,r,i,n){var s,o,a=8*n-i-1,c=(1<<a)-1,h=c>>1,u=-7,l=r?n-1:0,p=r?-1:1,f=t[e+l];for(l+=p,s=f&(1<<-u)-1,f>>=-u,u+=a;u>0;s=256*s+t[e+l],l+=p,u-=8);for(o=s&(1<<-u)-1,s>>=-u,u+=i;u>0;o=256*o+t[e+l],l+=p,u-=8);if(0===s)s=1-h;else{if(s===c)return o?NaN:1/0*(f?-1:1);o+=Math.pow(2,i),s-=h}return(f?-1:1)*o*Math.pow(2,s-i)},e.write=function(t,e,r,i,n,s){var o,a,c,h=8*s-n-1,u=(1<<h)-1,l=u>>1,p=23===n?Math.pow(2,-24)-Math.pow(2,-77):0,f=i?0:s-1,d=i?1:-1,g=e<0||0===e&&1/e<0?1:0;for(e=Math.abs(e),isNaN(e)||e===1/0?(a=isNaN(e)?1:0,o=u):(o=Math.floor(Math.log(e)/Math.LN2),e*(c=Math.pow(2,-o))<1&&(o--,c*=2),(e+=o+l>=1?p/c:p*Math.pow(2,1-l))*c>=2&&(o++,c/=2),o+l>=u?(a=0,o=u):o+l>=1?(a=(e*c-1)*Math.pow(2,n),o+=l):(a=e*Math.pow(2,l-1)*Math.pow(2,n),o=0));n>=8;t[r+f]=255&a,f+=d,a/=256,n-=8);for(o=o<<n|a,h+=n;h>0;t[r+f]=255&o,f+=d,o/=256,h-=8);t[r+f-d]|=128*g}},717:t=>{"function"==typeof Object.create?t.exports=function(t,e){e&&(t.super_=e,t.prototype=Object.create(e.prototype,{constructor:{value:t,enumerable:!1,writable:!0,configurable:!0}}))}:t.exports=function(t,e){if(e){t.super_=e;var r=function(){};r.prototype=e.prototype,t.prototype=new r,t.prototype.constructor=t}}},826:t=>{var e={}.toString;t.exports=Array.isArray||function(t){return"[object Array]"==e.call(t)}},205:t=>{t.exports=function(t){return t.replace(/[-\\^$*+?.()|[\]{}]/g,"\\$&")}},509:(t,e,r)=>{var i=r(764),n=i.Buffer;function s(t,e){for(var r in t)e[r]=t[r]}function o(t,e,r){return n(t,e,r)}n.from&&n.alloc&&n.allocUnsafe&&n.allocUnsafeSlow?t.exports=i:(s(i,e),e.Buffer=o),s(n,o),o.from=function(t,e,r){if("number"==typeof t)throw new TypeError("Argument must not be a number");return n(t,e,r)},o.alloc=function(t,e,r){if("number"!=typeof t)throw new TypeError("Argument must be a number");var i=n(t);return void 0!==e?"string"==typeof r?i.fill(e,r):i.fill(e):i.fill(0),i},o.allocUnsafe=function(t){if("number"!=typeof t)throw new TypeError("Argument must be a number");return n(t)},o.allocUnsafeSlow=function(t){if("number"!=typeof t)throw new TypeError("Argument must be a number");return i.SlowBuffer(t)}},981:(t,e,r)=>{var i=r(719),n=r(529),s=r(205);function o(t,e){t&&Object.keys(t).forEach((function(r){e(t[r],r)}))}function a(t,e){return{}.hasOwnProperty.call(t,e)}function c(t,e,r){var u="";function l(t,e){var r=this;this.tag=t,this.attribs=e||{},this.tagPosition=u.length,this.text="",this.updateParentNodeText=function(){y.length&&(y[y.length-1].text+=r.text)}}e?(e=n(c.defaults,e)).parser?e.parser=n(h,e.parser):e.parser=h:(e=c.defaults).parser=h;var p,f,d=e.nonTextTags||["script","style","textarea"];e.allowedAttributes&&(p={},f={},o(e.allowedAttributes,(function(t,e){p[e]=[];var r=[];t.forEach((function(t){t.indexOf("*")>=0?r.push(s(t).replace(/\\\*/g,".*")):p[e].push(t)})),f[e]=new RegExp("^("+r.join("|")+")$")})));var g={};o(e.allowedClasses,(function(t,e){p&&(a(p,e)||(p[e]=[]),p[e].push("class")),g[e]=t}));var _,m={};o(e.transformTags,(function(t,e){var r;"function"==typeof t?r=t:"string"==typeof t&&(r=c.simpleTransform(t)),"*"===e?_=r:m[e]=r}));var b=0,y=[],v={},w={},x=!1,S=0,E=new i.Parser({onopentag:function(t,r){if(x)S++;else{var i=new l(t,r);y.push(i);var n,s=!1,c=!!i.text;a(m,t)&&(n=m[t](t,r),i.attribs=r=n.attribs,void 0!==n.text&&(i.innerText=n.text),t!==n.tagName&&(i.name=t=n.tagName,w[b]=n.tagName)),_&&(n=_(t,r),i.attribs=r=n.attribs,t!==n.tagName&&(i.name=t=n.tagName,w[b]=n.tagName)),e.allowedTags&&-1===e.allowedTags.indexOf(t)&&(s=!0,-1!==d.indexOf(t)&&(x=!0,S=1),v[b]=!0),b++,s||(u+="<"+t,(!p||a(p,t)||p["*"])&&o(r,(function(r,n){if(!p||a(p,t)&&-1!==p[t].indexOf(n)||p["*"]&&-1!==p["*"].indexOf(n)||a(f,t)&&f[t].test(n)||f["*"]&&f["*"].test(n)){if(("href"===n||"src"===n)&&function(t,r){var i=(r=(r=r.replace(/[\x00-\x20]+/g,"")).replace(/<\!\-\-.*?\-\-\>/g,"")).match(/^([a-zA-Z]+)\:/);if(!i)return!1;var n=i[1].toLowerCase();return a(e.allowedSchemesByTag,t)?-1===e.allowedSchemesByTag[t].indexOf(n):!e.allowedSchemes||-1===e.allowedSchemes.indexOf(n)}(t,r))return void delete i.attribs[n];if("class"===n&&!(s=r,o=g[t],r=o?(s=s.split(/\s+/)).filter((function(t){return-1!==o.indexOf(t)})).join(" "):s).length)return void delete i.attribs[n];u+=" "+n,r.length&&(u+='="'+r+'"')}else delete i.attribs[n];var s,o})),-1!==e.selfClosing.indexOf(t)?u+=" />":(u+=">",!i.innerText||c||e.textFilter||(u+=i.innerText)))}},ontext:function(t){if(!x){var r,i=y[y.length-1];i&&(r=i.tag,t=void 0!==i.innerText?i.innerText:t),"script"===r||"style"===r?u+=t:e.textFilter?u+=e.textFilter(t):u+=t,y.length&&(y[y.length-1].text+=t)}},onclosetag:function(t){if(x){if(--S)return;x=!1}var r=y.pop();if(r){if(x=!1,b--,v[b])return delete v[b],void r.updateParentNodeText();w[b]&&(t=w[b],delete w[b]),e.exclusiveFilter&&e.exclusiveFilter(r)?u=u.substr(0,r.tagPosition):(r.updateParentNodeText(),-1===e.selfClosing.indexOf(t)&&(u+="</"+t+">"))}}},e.parser);return E.write(t),E.end(),u}t.exports=c;var h={decodeEntities:!0};c.defaults={allowedTags:["h3","h4","h5","h6","blockquote","p","a","ul","ol","nl","li","b","i","strong","em","strike","code","hr","br","div","table","thead","caption","tbody","tr","th","td","pre"],allowedAttributes:{a:["href","name","target"],img:["src"]},selfClosing:["img","br","hr","area","base","basefont","input","link","meta"],allowedSchemes:["http","https","ftp","mailto"],allowedSchemesByTag:{}},c.simpleTransform=function(t,e,r){return r=void 0===r||r,e=e||{},function(i,n){var s;if(r)for(s in e)n[s]=e[s];else n=e;return{tagName:t,attribs:n}}}},553:(t,e,r)=>{"use strict";var i=r(509).Buffer,n=i.isEncoding||function(t){switch((t=""+t)&&t.toLowerCase()){case"hex":case"utf8":case"utf-8":case"ascii":case"binary":case"base64":case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":case"raw":return!0;default:return!1}};function s(t){var e;switch(this.encoding=function(t){var e=function(t){if(!t)return"utf8";for(var e;;)switch(t){case"utf8":case"utf-8":return"utf8";case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return"utf16le";case"latin1":case"binary":return"latin1";case"base64":case"ascii":case"hex":return t;default:if(e)return;t=(""+t).toLowerCase(),e=!0}}(t);if("string"!=typeof e&&(i.isEncoding===n||!n(t)))throw new Error("Unknown encoding: "+t);return e||t}(t),this.encoding){case"utf16le":this.text=c,this.end=h,e=4;break;case"utf8":this.fillLast=a,e=4;break;case"base64":this.text=u,this.end=l,e=3;break;default:return this.write=p,void(this.end=f)}this.lastNeed=0,this.lastTotal=0,this.lastChar=i.allocUnsafe(e)}function o(t){return t<=127?0:t>>5==6?2:t>>4==14?3:t>>3==30?4:t>>6==2?-1:-2}function a(t){var e=this.lastTotal-this.lastNeed,r=function(t,e,r){if(128!=(192&e[0]))return t.lastNeed=0,"�";if(t.lastNeed>1&&e.length>1){if(128!=(192&e[1]))return t.lastNeed=1,"�";if(t.lastNeed>2&&e.length>2&&128!=(192&e[2]))return t.lastNeed=2,"�"}}(this,t);return void 0!==r?r:this.lastNeed<=t.length?(t.copy(this.lastChar,e,0,this.lastNeed),this.lastChar.toString(this.encoding,0,this.lastTotal)):(t.copy(this.lastChar,e,0,t.length),void(this.lastNeed-=t.length))}function c(t,e){if((t.length-e)%2==0){var r=t.toString("utf16le",e);if(r){var i=r.charCodeAt(r.length-1);if(i>=55296&&i<=56319)return this.lastNeed=2,this.lastTotal=4,this.lastChar[0]=t[t.length-2],this.lastChar[1]=t[t.length-1],r.slice(0,-1)}return r}return this.lastNeed=1,this.lastTotal=2,this.lastChar[0]=t[t.length-1],t.toString("utf16le",e,t.length-1)}function h(t){var e=t&&t.length?this.write(t):"";if(this.lastNeed){var r=this.lastTotal-this.lastNeed;return e+this.lastChar.toString("utf16le",0,r)}return e}function u(t,e){var r=(t.length-e)%3;return 0===r?t.toString("base64",e):(this.lastNeed=3-r,this.lastTotal=3,1===r?this.lastChar[0]=t[t.length-1]:(this.lastChar[0]=t[t.length-2],this.lastChar[1]=t[t.length-1]),t.toString("base64",e,t.length-r))}function l(t){var e=t&&t.length?this.write(t):"";return this.lastNeed?e+this.lastChar.toString("base64",0,3-this.lastNeed):e}function p(t){return t.toString(this.encoding)}function f(t){return t&&t.length?this.write(t):""}e.s=s,s.prototype.write=function(t){if(0===t.length)return"";var e,r;if(this.lastNeed){if(void 0===(e=this.fillLast(t)))return"";r=this.lastNeed,this.lastNeed=0}else r=0;return r<t.length?e?e+this.text(t,r):this.text(t,r):e||""},s.prototype.end=function(t){var e=t&&t.length?this.write(t):"";return this.lastNeed?e+"�":e},s.prototype.text=function(t,e){var r=function(t,e,r){var i=e.length-1;if(i<r)return 0;var n=o(e[i]);return n>=0?(n>0&&(t.lastNeed=n-1),n):--i<r||-2===n?0:(n=o(e[i]))>=0?(n>0&&(t.lastNeed=n-2),n):--i<r||-2===n?0:(n=o(e[i]))>=0?(n>0&&(2===n?n=0:t.lastNeed=n-3),n):0}(this,t,e);if(!this.lastNeed)return t.toString("utf8",e);this.lastTotal=r;var i=t.length-(r-this.lastNeed);return t.copy(this.lastChar,0,i),t.toString("utf8",e,i)},s.prototype.fillLast=function(t){if(this.lastNeed<=t.length)return t.copy(this.lastChar,this.lastTotal-this.lastNeed,0,this.lastNeed),this.lastChar.toString(this.encoding,0,this.lastTotal);t.copy(this.lastChar,this.lastTotal-this.lastNeed,0,t.length),this.lastNeed-=t.length}},529:t=>{t.exports=function(){for(var t={},r=0;r<arguments.length;r++){var i=arguments[r];for(var n in i)e.call(i,n)&&(t[n]=i[n])}return t};var e=Object.prototype.hasOwnProperty},994:()=>{}},e={};function r(i){if(e[i])return e[i].exports;var n=e[i]={exports:{}};return t[i](n,n.exports,r),n.exports}r.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return r.d(e,{a:e}),e},r.d=(t,e)=>{for(var i in e)r.o(e,i)&&!r.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},r.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),r.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),(()=>{"use strict";var t=r(981),e=r.n(t);Window.sanitizeHtml=e()})()})();
/*!
 * mustache.js - Logic-less {{mustache}} templates with JavaScript
 * http://github.com/janl/mustache.js
 */

/*global define: false*/

(function (global, factory) {
  if (typeof exports === "object" && exports) {
    factory(exports); // CommonJS
  } else if (typeof define === "function" && define.amd) {
    define(['exports'], factory); // AMD
  } else {
    factory(global.Mustache = {}); // <script>
  }
}(this, function (mustache) {

  var Object_toString = Object.prototype.toString;
  var isArray = Array.isArray || function (object) {
    return Object_toString.call(object) === '[object Array]';
  };

  function isFunction(object) {
    return typeof object === 'function';
  }

  function escapeRegExp(string) {
    return string.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&");
  }

  // Workaround for https://issues.apache.org/jira/browse/COUCHDB-577
  // See https://github.com/janl/mustache.js/issues/189
  var RegExp_test = RegExp.prototype.test;
  function testRegExp(re, string) {
    return RegExp_test.call(re, string);
  }

  var nonSpaceRe = /\S/;
  function isWhitespace(string) {
    return !testRegExp(nonSpaceRe, string);
  }

  var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
  };

  function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
      return entityMap[s];
    });
  }

  var whiteRe = /\s*/;
  var spaceRe = /\s+/;
  var equalsRe = /\s*=/;
  var curlyRe = /\s*\}/;
  var tagRe = /#|\^|\/|>|\{|&|=|!/;

  /**
   * Breaks up the given `template` string into a tree of tokens. If the `tags`
   * argument is given here it must be an array with two string values: the
   * opening and closing tags used in the template (e.g. [ "<%", "%>" ]). Of
   * course, the default is to use mustaches (i.e. mustache.tags).
   *
   * A token is an array with at least 4 elements. The first element is the
   * mustache symbol that was used inside the tag, e.g. "#" or "&". If the tag
   * did not contain a symbol (i.e. {{myValue}}) this element is "name". For
   * all text that appears outside a symbol this element is "text".
   *
   * The second element of a token is its "value". For mustache tags this is
   * whatever else was inside the tag besides the opening symbol. For text tokens
   * this is the text itself.
   *
   * The third and fourth elements of the token are the start and end indices,
   * respectively, of the token in the original template.
   *
   * Tokens that are the root node of a subtree contain two more elements: 1) an
   * array of tokens in the subtree and 2) the index in the original template at
   * which the closing tag for that section begins.
   */
  function parseTemplate(template, tags) {
    if (!template)
      return [];

    var sections = [];     // Stack to hold section tokens
    var tokens = [];       // Buffer to hold the tokens
    var spaces = [];       // Indices of whitespace tokens on the current line
    var hasTag = false;    // Is there a {{tag}} on the current line?
    var nonSpace = false;  // Is there a non-space char on the current line?

    // Strips all whitespace tokens array for the current line
    // if there was a {{#tag}} on it and otherwise only space.
    function stripSpace() {
      if (hasTag && !nonSpace) {
        while (spaces.length)
          delete tokens[spaces.pop()];
      } else {
        spaces = [];
      }

      hasTag = false;
      nonSpace = false;
    }

    var openingTagRe, closingTagRe, closingCurlyRe;
    function compileTags(tags) {
      if (typeof tags === 'string')
        tags = tags.split(spaceRe, 2);

      if (!isArray(tags) || tags.length !== 2)
        throw new Error('Invalid tags: ' + tags);

      openingTagRe = new RegExp(escapeRegExp(tags[0]) + '\\s*');
      closingTagRe = new RegExp('\\s*' + escapeRegExp(tags[1]));
      closingCurlyRe = new RegExp('\\s*' + escapeRegExp('}' + tags[1]));
    }

    compileTags(tags || mustache.tags);

    var scanner = new Scanner(template);

    var start, type, value, chr, token, openSection;
    while (!scanner.eos()) {
      start = scanner.pos;

      // Match any text between tags.
      value = scanner.scanUntil(openingTagRe);

      if (value) {
        for (var i = 0, valueLength = value.length; i < valueLength; ++i) {
          chr = value.charAt(i);

          if (isWhitespace(chr)) {
            spaces.push(tokens.length);
          } else {
            nonSpace = true;
          }

          tokens.push([ 'text', chr, start, start + 1 ]);
          start += 1;

          // Check for whitespace on the current line.
          if (chr === '\n')
            stripSpace();
        }
      }

      // Match the opening tag.
      if (!scanner.scan(openingTagRe))
        break;

      hasTag = true;

      // Get the tag type.
      type = scanner.scan(tagRe) || 'name';
      scanner.scan(whiteRe);

      // Get the tag value.
      if (type === '=') {
        value = scanner.scanUntil(equalsRe);
        scanner.scan(equalsRe);
        scanner.scanUntil(closingTagRe);
      } else if (type === '{') {
        value = scanner.scanUntil(closingCurlyRe);
        scanner.scan(curlyRe);
        scanner.scanUntil(closingTagRe);
        type = '&';
      } else {
        value = scanner.scanUntil(closingTagRe);
      }

      // Match the closing tag.
      if (!scanner.scan(closingTagRe))
        throw new Error('Unclosed tag at ' + scanner.pos);

      token = [ type, value, start, scanner.pos ];
      tokens.push(token);

      if (type === '#' || type === '^') {
        sections.push(token);
      } else if (type === '/') {
        // Check section nesting.
        openSection = sections.pop();

        if (!openSection)
          throw new Error('Unopened section "' + value + '" at ' + start);

        if (openSection[1] !== value)
          throw new Error('Unclosed section "' + openSection[1] + '" at ' + start);
      } else if (type === 'name' || type === '{' || type === '&') {
        nonSpace = true;
      } else if (type === '=') {
        // Set the tags for the next time around.
        compileTags(value);
      }
    }

    // Make sure there are no open sections when we're done.
    openSection = sections.pop();

    if (openSection)
      throw new Error('Unclosed section "' + openSection[1] + '" at ' + scanner.pos);

    return nestTokens(squashTokens(tokens));
  }

  /**
   * Combines the values of consecutive text tokens in the given `tokens` array
   * to a single token.
   */
  function squashTokens(tokens) {
    var squashedTokens = [];

    var token, lastToken;
    for (var i = 0, numTokens = tokens.length; i < numTokens; ++i) {
      token = tokens[i];

      if (token) {
        if (token[0] === 'text' && lastToken && lastToken[0] === 'text') {
          lastToken[1] += token[1];
          lastToken[3] = token[3];
        } else {
          squashedTokens.push(token);
          lastToken = token;
        }
      }
    }

    return squashedTokens;
  }

  /**
   * Forms the given array of `tokens` into a nested tree structure where
   * tokens that represent a section have two additional items: 1) an array of
   * all tokens that appear in that section and 2) the index in the original
   * template that represents the end of that section.
   */
  function nestTokens(tokens) {
    var nestedTokens = [];
    var collector = nestedTokens;
    var sections = [];

    var token, section;
    for (var i = 0, numTokens = tokens.length; i < numTokens; ++i) {
      token = tokens[i];

      switch (token[0]) {
      case '#':
      case '^':
        collector.push(token);
        sections.push(token);
        collector = token[4] = [];
        break;
      case '/':
        section = sections.pop();
        section[5] = token[2];
        collector = sections.length > 0 ? sections[sections.length - 1][4] : nestedTokens;
        break;
      default:
        collector.push(token);
      }
    }

    return nestedTokens;
  }

  /**
   * A simple string scanner that is used by the template parser to find
   * tokens in template strings.
   */
  function Scanner(string) {
    this.string = string;
    this.tail = string;
    this.pos = 0;
  }

  /**
   * Returns `true` if the tail is empty (end of string).
   */
  Scanner.prototype.eos = function () {
    return this.tail === "";
  };

  /**
   * Tries to match the given regular expression at the current position.
   * Returns the matched text if it can match, the empty string otherwise.
   */
  Scanner.prototype.scan = function (re) {
    var match = this.tail.match(re);

    if (!match || match.index !== 0)
      return '';

    var string = match[0];

    this.tail = this.tail.substring(string.length);
    this.pos += string.length;

    return string;
  };

  /**
   * Skips all text until the given regular expression can be matched. Returns
   * the skipped string, which is the entire tail if no match can be made.
   */
  Scanner.prototype.scanUntil = function (re) {
    var index = this.tail.search(re), match;

    switch (index) {
    case -1:
      match = this.tail;
      this.tail = "";
      break;
    case 0:
      match = "";
      break;
    default:
      match = this.tail.substring(0, index);
      this.tail = this.tail.substring(index);
    }

    this.pos += match.length;

    return match;
  };

  /**
   * Represents a rendering context by wrapping a view object and
   * maintaining a reference to the parent context.
   */
  function Context(view, parentContext) {
    this.view = view == null ? {} : view;
    this.cache = { '.': this.view };
    this.parent = parentContext;
  }

  /**
   * Creates a new context using the given view with this context
   * as the parent.
   */
  Context.prototype.push = function (view) {
    return new Context(view, this);
  };

  /**
   * Returns the value of the given name in this context, traversing
   * up the context hierarchy if the value is absent in this context's view.
   */
  Context.prototype.lookup = function (name) {
    var cache = this.cache;
    var value;
    if (name in cache) {
      value = cache[name];
    } else {
      var context = this, names, index;

      while (context) {
        if (name.indexOf('.') > 0) {
          value = context.view;
          names = name.split('.');
          index = 0;

          while (value != null && index < names.length)
            value = value[names[index++]];
        } else if (typeof context.view == 'object') {
          value = context.view[name];
        }

        if (value != null)
          break;

        context = context.parent;
      }

      cache[name] = value;
    }

    if (isFunction(value))
      value = value.call(this.view);

    return value;
  };

  /**
   * A Writer knows how to take a stream of tokens and render them to a
   * string, given a context. It also maintains a cache of templates to
   * avoid the need to parse the same template twice.
   */
  function Writer() {
    this.cache = {};
  }

  /**
   * Clears all cached templates in this writer.
   */
  Writer.prototype.clearCache = function () {
    this.cache = {};
  };

  /**
   * Parses and caches the given `template` and returns the array of tokens
   * that is generated from the parse.
   */
  Writer.prototype.parse = function (template, tags) {
    var cache = this.cache;
    var tokens = cache[template];

    if (tokens == null)
      tokens = cache[template] = parseTemplate(template, tags);

    return tokens;
  };

  /**
   * High-level method that is used to render the given `template` with
   * the given `view`.
   *
   * The optional `partials` argument may be an object that contains the
   * names and templates of partials that are used in the template. It may
   * also be a function that is used to load partial templates on the fly
   * that takes a single argument: the name of the partial.
   */
  Writer.prototype.render = function (template, view, partials) {
    var tokens = this.parse(template);
    var context = (view instanceof Context) ? view : new Context(view);
    return this.renderTokens(tokens, context, partials, template);
  };

  /**
   * Low-level method that renders the given array of `tokens` using
   * the given `context` and `partials`.
   *
   * Note: The `originalTemplate` is only ever used to extract the portion
   * of the original template that was contained in a higher-order section.
   * If the template doesn't use higher-order sections, this argument may
   * be omitted.
   */
  Writer.prototype.renderTokens = function (tokens, context, partials, originalTemplate) {
    var buffer = '';

    // This function is used to render an arbitrary template
    // in the current context by higher-order sections.
    var self = this;
    function subRender(template) {
      return self.render(template, context, partials);
    }

    var token, value;
    for (var i = 0, numTokens = tokens.length; i < numTokens; ++i) {
      token = tokens[i];

      switch (token[0]) {
      case '#':
        //Custom for Roll20: Allow doing thigns like #rollWasCrit() <funciton argument>
        var funcWithArgsCheck = (token[1] + "").split(" ");
        if(funcWithArgsCheck[0].substring(funcWithArgsCheck[0].length - 2, funcWithArgsCheck[0].length) === "()") {
          value = context.lookup(funcWithArgsCheck[0]);
          funcWithArgsCheck.splice(0, 1); //remove name of func from args.
        }
        else {    
          value = context.lookup(token[1]);
        }

        if (!value)
          continue;

        if (isArray(value)) {
          for (var j = 0, valueLength = value.length; j < valueLength; ++j) {
            buffer += this.renderTokens(token[4], context.push(value[j]), partials, originalTemplate);
          }
        } else if (typeof value === 'object' || typeof value === 'string') {
          buffer += this.renderTokens(token[4], context.push(value), partials, originalTemplate);
        } else if (isFunction(value)) {
          if (typeof originalTemplate !== 'string')
            throw new Error('Cannot use higher-order sections without the original template');

          // Extract the portion of the original template that the section contains.
          value = value.call(context.view, originalTemplate.slice(token[3], token[5]), subRender, funcWithArgsCheck);

          if (value != null)
            buffer += value;
        } else {
          buffer += this.renderTokens(token[4], context, partials, originalTemplate);
        }

        break;
      case '^':
        value = context.lookup(token[1]);

        // Use JavaScript's definition of falsy. Include empty arrays.
        // See https://github.com/janl/mustache.js/issues/186
        if (!value || (isArray(value) && value.length === 0))
          buffer += this.renderTokens(token[4], context, partials, originalTemplate);

        break;
      case '>':
        if (!partials)
          continue;

        value = isFunction(partials) ? partials(token[1]) : partials[token[1]];

        if (value != null)
          buffer += this.renderTokens(this.parse(value), context, partials, value);

        break;
      case '&':
        value = context.lookup(token[1]);

        if (value != null)
          buffer += value;

        break;
      case 'name':
        value = context.lookup(token[1]);

        if (value != null) {
          //buffer += mustache.escape(value);
          buffer += value;
        }

        break;
      case 'text':
        buffer += token[1];
        break;
      }
    }

    return buffer;
  };

  mustache.name = "mustache.js";
  mustache.version = "1.0.0";
  mustache.tags = [ "{{", "}}" ];

  // All high-level mustache.* functions use this writer.
  var defaultWriter = new Writer();

  /**
   * Clears all cached templates in the default writer.
   */
  mustache.clearCache = function () {
    return defaultWriter.clearCache();
  };

  /**
   * Parses and caches the given template in the default writer and returns the
   * array of tokens it contains. Doing this ahead of time avoids the need to
   * parse templates on the fly as they are rendered.
   */
  mustache.parse = function (template, tags) {
    return defaultWriter.parse(template, tags);
  };

  /**
   * Renders the `template` with the given `view` and `partials` using the
   * default writer.
   */
  mustache.render = function (template, view, partials) {
    return defaultWriter.render(template, view, partials);
  };

  // This is here for backwards compatibility with 0.4.x.
  mustache.to_html = function (template, view, partials, send) {
    var result = mustache.render(template, view, partials);

    if (isFunction(send)) {
      send(result);
    } else {
      return result;
    }
  };

  // Export the escaping function so that the user may override it.
  // See https://github.com/janl/mustache.js/issues/244
  mustache.escape = escapeHtml;

  // Export these mainly for testing, but also for advanced usage.
  mustache.Scanner = Scanner;
  mustache.Context = Context;
  mustache.Writer = Writer;

}));
(function() {
    window.Markdown = {
        parse: function (s) {
            var r = s, ii, pre1 = [], pre2 = [];

            // detect newline format
            var newline = r.indexOf('\r\n') != -1 ? '\r\n' : r.indexOf('\n') != -1 ? '\n' : ''
            
            // store {{{ unformatted blocks }}} and <pre> pre-formatted blocks </pre>
            r = r.replace(/{{{([\s\S]*?)}}}/g, function (x) { pre1.push(x.substring(3, x.length - 3)); return '{{{}}}'; });
            r = r.replace(new RegExp('<pre>([\\s\\S]*?)</pre>', 'gi'), function (x) { pre2.push(x.substring(5, x.length - 6)); return '<pre></pre>'; });
            
            // h1 - h4 and hr
            // r = r.replace(/^==== (.*)=*/gm, '<h4>$1</h4>');
            // r = r.replace(/^=== (.*)=*/gm, '<h3>$1</h3>');
            // r = r.replace(/^== (.*)=*/gm, '<h2>$1</h2>');
            // r = r.replace(/^= (.*)=*/gm, '<h1>$1</h1>');
            // r = r.replace(/^[-*][-*][-*]+/gm, '<hr>');
            
            // bold, italics, and code formatting
            r = r.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            //r = r.replace(new RegExp('//(((?!https?://).)*?)//', 'g'), '<em>$1</em>');
            r = r.replace(/\*(.*?)\*/g, '<em>$1</em>');
            r = r.replace(/``(.*?)``/g, '<code>$1</code>');
            
            // unordered lists
            // r = r.replace(/^\*\*\*\* (.*)/gm, '<ul><ul><ul><ul><li>$1</li></ul></ul></ul></ul>');
            // r = r.replace(/^\*\*\* (.*)/gm, '<ul><ul><ul><li>$1</li></ul></ul></ul>');
            // r = r.replace(/^\*\* (.*)/gm, '<ul><ul><li>$1</li></ul></ul>');
            // r = r.replace(/^\* (.*)/gm, '<ul><li>$1</li></ul>');
            // for (ii = 0; ii < 3; ii++) r = r.replace(new RegExp('</ul>' + newline + '<ul>', 'g'), newline);
            
            // ordered lists
            // r = r.replace(/^#### (.*)/gm, '<ol><ol><ol><ol><li>$1</li></ol></ol></ol></ol>');
            // r = r.replace(/^### (.*)/gm, '<ol><ol><ol><li>$1</li></ol></ol></ol>');
            // r = r.replace(/^## (.*)/gm, '<ol><ol><li>$1</li></ol></ol>');
            // r = r.replace(/^# (.*)/gm, '<ol><li>$1</li></ol>');
            // for (ii = 0; ii < 3; ii++) r = r.replace(new RegExp('</ol>' + newline + '<ol>', 'g'), newline);
            
            // links
            r = r.replace(/\[([^\]]+)\]\(([^)]+(\.png|\.gif|\.jpg|\.jpeg))\)/g, '<a href="$2"><img src="$2" alt="$1" /></a>');
            r = r.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
            //r = r.replace(/\[\[([^\]|]*?)\]\]/g, '<a href="$1">$1</a>');
            //r = r.replace(/\[\[([^|]*?)\|(.*?)\]\]/g, '<a href="$1">$2</a>');
            
            // images
            // r = r.replace(/{{([^\]|]*?)}}/g, '<img src="$1">');
            // r = r.replace(/{{([^|]*?)\|(.*?)}}/g, '<img src="$1" alt="$2">');
            
            // video
            // r = r.replace(/<<(.*?)>>/g, '<embed class="video" src="$1" allowfullscreen="true" allowscriptaccess="never" type="application/x-shockwave/flash"></embed>');
            
            // hard linebreak if there are 2 or more spaces at the end of a line
            // r = r.replace(new RegExp(' + ' + newline, 'g'), '<br>' + newline);
            
            // split on double-newlines, then add paragraph tags when the first tag isn't a block level element

            // var blockLevelElements = ["p", "div", "pre", "ul", "table", "ol", "blockquote"];

            // if (newline != '') for (var p = r.split(newline + newline), i = 0; i < p.length; i++) {
            //     var blockLevel = false;
            //     if (p[i].length >= 1 && p[i].charAt(0) == '<') {
            //         // check if the first tag is a block-level element
            //         var firstSpace = p[i].indexOf(' '), firstCloseTag = p[i].indexOf('>');
            //         var endIndex = firstSpace > -1 && firstCloseTag > -1 ? Math.min(firstSpace, firstCloseTag) : firstSpace > -1 ? firstSpace : firstCloseTag;
            //         var tag = p[i].substring(1, endIndex).toLowerCase();
            //         for (var j = 0; j < blockLevelElements.length; j++) if (blockLevelElements[j] == tag) blockLevel = true;
            //     } else if (p[i].length >= 1 && p[i].charAt(0) == '|') {
            //         // format the paragraph as a table
            //         blockLevel = true;
            //         p[i] = p[i].replace(/ \|= /g, '</th><th>').replace(/\|= /g, '<tr><th>').replace(/ \|=/g, '</th></tr>');
            //         p[i] = p[i].replace(/ \| /g, '</td><td>').replace(/\| /g, '<tr><td>').replace(/ \|/g, '</td></tr>');
            //         p[i] = '<table>' + p[i] + '</table>';
            //     } else if (p[i].length >= 2 && p[i].charAt(0) == '>' && p[i].charAt(1) == ' ') {
            //         // format the paragraph as a blockquote
            //         blockLevel = true;
            //         p[i] = '<blockquote>' + p[i].replace(/^> /gm, '') + '</blockquote>';
            //     }
            //     if (!blockLevel) p[i] = '<p>' + p[i] + '</p>';
            // }
            
            // reassemble the paragraphs
            // if (newline != '') r = p.join(newline + newline);
            
            // restore the preformatted and unformatted blocks
            r = r.replace(new RegExp('<pre></pre>', 'g'), function (match) { return '<pre>' + pre2.shift() + '</pre>'; });
            r = r.replace(/{{{}}}/g, function (match) { return pre1.shift(); });
            return r;
        }
    };
})();
/*
 *  Sugar Library v1.4.1
 *
 *  Freely distributable and licensed under the MIT-style license.
 *  Copyright (c) 2013 Andrew Plummer
 *  http://sugarjs.com/
 *
 * ---------------------------- */
(function(){function aa(a){return function(){return a}}
var m=Object,p=Array,q=RegExp,r=Date,s=String,t=Number,u=Math,ba="undefined"!==typeof global?global:this,v=m.prototype.toString,da=m.prototype.hasOwnProperty,ea=m.defineProperty&&m.defineProperties,fa="function"===typeof q(),ga=!("0"in new s("a")),ia={},ja=/^\[object Date|Array|String|Number|RegExp|Boolean|Arguments\]$/,w="Boolean Number String Array Date RegExp Function".split(" "),la=ka("boolean",w[0]),y=ka("number",w[1]),z=ka("string",w[2]),A=ma(w[3]),C=ma(w[4]),D=ma(w[5]),F=ma(w[6]);
function ma(a){var b="Array"===a&&p.isArray||function(b,d){return(d||v.call(b))==="[object "+a+"]"};return ia[a]=b}function ka(a,b){function c(c){return G(c)?v.call(c)==="[object "+b+"]":typeof c===a}return ia[b]=c}
function na(a){a.SugarMethods||(oa(a,"SugarMethods",{}),H(a,!1,!0,{extend:function(b,c,d){H(a,!1!==d,c,b)},sugarRestore:function(){return pa(this,a,arguments,function(a,c,d){oa(a,c,d.method)})},sugarRevert:function(){return pa(this,a,arguments,function(a,c,d){d.existed?oa(a,c,d.original):delete a[c]})}}))}function H(a,b,c,d){var e=b?a.prototype:a;na(a);I(d,function(d,f){var h=e[d],l=J(e,d);F(c)&&h&&(f=qa(h,f,c));!1===c&&h||oa(e,d,f);a.SugarMethods[d]={method:f,existed:l,original:h,instance:b}})}
function K(a,b,c,d,e){var g={};d=z(d)?d.split(","):d;d.forEach(function(a,b){e(g,a,b)});H(a,b,c,g)}function pa(a,b,c,d){var e=0===c.length,g=L(c),f=!1;I(b.SugarMethods,function(b,c){if(e||-1!==g.indexOf(b))f=!0,d(c.instance?a.prototype:a,b,c)});return f}function qa(a,b,c){return function(d){return c.apply(this,arguments)?b.apply(this,arguments):a.apply(this,arguments)}}function oa(a,b,c){ea?m.defineProperty(a,b,{value:c,configurable:!0,enumerable:!1,writable:!0}):a[b]=c}
function L(a,b,c){var d=[];c=c||0;var e;for(e=a.length;c<e;c++)d.push(a[c]),b&&b.call(a,a[c],c);return d}function sa(a,b,c){var d=a[c||0];A(d)&&(a=d,c=0);L(a,b,c)}function ta(a){if(!a||!a.call)throw new TypeError("Callback is not callable");}function M(a){return void 0!==a}function N(a){return void 0===a}function J(a,b){return!!a&&da.call(a,b)}function G(a){return!!a&&("object"===typeof a||fa&&D(a))}function ua(a){var b=typeof a;return null==a||"string"===b||"number"===b||"boolean"===b}
function va(a,b){b=b||v.call(a);try{if(a&&a.constructor&&!J(a,"constructor")&&!J(a.constructor.prototype,"isPrototypeOf"))return!1}catch(c){return!1}return!!a&&"[object Object]"===b&&"hasOwnProperty"in a}function I(a,b){for(var c in a)if(J(a,c)&&!1===b.call(a,c,a[c],a))break}function wa(a,b){for(var c=0;c<a;c++)b(c)}function xa(a,b){I(b,function(c){a[c]=b[c]});return a}function ya(a){ua(a)&&(a=m(a));if(ga&&z(a))for(var b=a,c=0,d;d=b.charAt(c);)b[c++]=d;return a}function O(a){xa(this,ya(a))}
O.prototype.constructor=m;var P=u.abs,za=u.pow,Aa=u.ceil,Q=u.floor,R=u.round,Ca=u.min,S=u.max;function Da(a,b,c){var d=za(10,P(b||0));c=c||R;0>b&&(d=1/d);return c(a*d)/d}var Ea=48,Fa=57,Ga=65296,Ha=65305,Ia=".",Ja="",Ka={},La;function Ma(){return"\t\n\x0B\f\r \u00a0\u1680\u180e\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u2028\u2029\u3000\ufeff"}function Na(a,b){var c="";for(a=a.toString();0<b;)if(b&1&&(c+=a),b>>=1)a+=a;return c}
function Oa(a,b){var c,d;c=a.replace(La,function(a){a=Ka[a];a===Ia&&(d=!0);return a});return d?parseFloat(c):parseInt(c,b||10)}function T(a,b,c,d){d=P(a).toString(d||10);d=Na("0",b-d.replace(/\.\d+/,"").length)+d;if(c||0>a)d=(0>a?"-":"+")+d;return d}function Pa(a){if(11<=a&&13>=a)return"th";switch(a%10){case 1:return"st";case 2:return"nd";case 3:return"rd";default:return"th"}}
function Qa(a,b){function c(a,c){if(a||-1<b.indexOf(c))d+=c}var d="";b=b||"";c(a.multiline,"m");c(a.ignoreCase,"i");c(a.global,"g");c(a.u,"y");return d}function Ra(a){z(a)||(a=s(a));return a.replace(/([\\/\'*+?|()\[\]{}.^$])/g,"\\$1")}function U(a,b){return a["get"+(a._utc?"UTC":"")+b]()}function Sa(a,b,c){return a["set"+(a._utc&&"ISOWeek"!=b?"UTC":"")+b](c)}
function Ta(a,b){var c=typeof a,d,e,g,f,h,l,n;if("string"===c)return a;g=v.call(a);d=va(a,g);e=A(a,g);if(null!=a&&d||e){b||(b=[]);if(1<b.length)for(l=b.length;l--;)if(b[l]===a)return"CYC";b.push(a);d=a.valueOf()+s(a.constructor);f=e?a:m.keys(a).sort();l=0;for(n=f.length;l<n;l++)h=e?l:f[l],d+=h+Ta(a[h],b);b.pop()}else d=-Infinity===1/a?"-0":s(a&&a.valueOf?a.valueOf():a);return c+g+d}function Ua(a,b){return a===b?0!==a||1/a===1/b:Va(a)&&Va(b)?Ta(a)===Ta(b):!1}
function Va(a){var b=v.call(a);return ja.test(b)||va(a,b)}function Wa(a,b,c){var d,e=a.length,g=b.length,f=!1!==b[g-1];if(!(g>(f?1:2)))return Xa(a,e,b[0],f,c);d=[];L(b,function(b){if(la(b))return!1;d.push(Xa(a,e,b,f,c))});return d}function Xa(a,b,c,d,e){d&&(c%=b,0>c&&(c=b+c));return e?a.charAt(c):a[c]}function Ya(a,b){K(b,!0,!1,a,function(a,b){a[b+("equal"===b?"s":"")]=function(){return m[b].apply(null,[this].concat(L(arguments)))}})}na(m);I(w,function(a,b){na(ba[b])});var Za,$a;
for($a=0;9>=$a;$a++)Za=s.fromCharCode($a+Ga),Ja+=Za,Ka[Za]=s.fromCharCode($a+Ea);Ka[","]="";Ka["\uff0e"]=Ia;Ka[Ia]=Ia;La=q("["+Ja+"\uff0e,"+Ia+"]","g");
"use strict";H(m,!1,!1,{keys:function(a){var b=[];if(!G(a)&&!D(a)&&!F(a))throw new TypeError("Object required");I(a,function(a){b.push(a)});return b}});
function ab(a,b,c,d){var e=a.length,g=-1==d,f=g?e-1:0;c=isNaN(c)?f:parseInt(c>>0);0>c&&(c=e+c);if(!g&&0>c||g&&c>=e)c=f;for(;g&&0<=c||!g&&c<e;){if(a[c]===b)return c;c+=d}return-1}function bb(a,b,c,d){var e=a.length,g=0,f=M(c);ta(b);if(0!=e||f)f||(c=a[d?e-1:g],g++);else throw new TypeError("Reduce called on empty array with no initial value");for(;g<e;)f=d?e-g-1:g,f in a&&(c=b(c,a[f],f,a)),g++;return c}function cb(a){if(0===a.length)throw new TypeError("First argument must be defined");}H(p,!1,!1,{isArray:function(a){return A(a)}});
H(p,!0,!1,{every:function(a,b){var c=this.length,d=0;for(cb(arguments);d<c;){if(d in this&&!a.call(b,this[d],d,this))return!1;d++}return!0},some:function(a,b){var c=this.length,d=0;for(cb(arguments);d<c;){if(d in this&&a.call(b,this[d],d,this))return!0;d++}return!1},map:function(a,b){b=arguments[1];var c=this.length,d=0,e=Array(c);for(cb(arguments);d<c;)d in this&&(e[d]=a.call(b,this[d],d,this)),d++;return e},filter:function(a){var b=arguments[1],c=this.length,d=0,e=[];for(cb(arguments);d<c;)d in
this&&a.call(b,this[d],d,this)&&e.push(this[d]),d++;return e},indexOf:function(a,b){return z(this)?this.indexOf(a,b):ab(this,a,b,1)},lastIndexOf:function(a,b){return z(this)?this.lastIndexOf(a,b):ab(this,a,b,-1)},forEach:function(a,b){var c=this.length,d=0;for(ta(a);d<c;)d in this&&a.call(b,this[d],d,this),d++},reduce:function(a,b){return bb(this,a,b)},reduceRight:function(a,b){return bb(this,a,b,!0)}});
H(Function,!0,!1,{bind:function(a){var b=this,c=L(arguments,null,1),d;if(!F(this))throw new TypeError("Function.prototype.bind called on a non-function");d=function(){return b.apply(b.prototype&&this instanceof b?this:a,c.concat(L(arguments)))};d.prototype=this.prototype;return d}});H(r,!1,!1,{now:function(){return(new r).getTime()}});
(function(){var a=Ma().match(/^\s+$/);try{s.prototype.trim.call([1])}catch(b){a=!1}H(s,!0,!a,{trim:function(){return this.toString().trimLeft().trimRight()},trimLeft:function(){return this.replace(q("^["+Ma()+"]+"),"")},trimRight:function(){return this.replace(q("["+Ma()+"]+$"),"")}})})();
(function(){var a=new r(r.UTC(1999,11,31)),a=a.toISOString&&"1999-12-31T00:00:00.000Z"===a.toISOString();K(r,!0,!a,"toISOString,toJSON",function(a,c){a[c]=function(){return T(this.getUTCFullYear(),4)+"-"+T(this.getUTCMonth()+1,2)+"-"+T(this.getUTCDate(),2)+"T"+T(this.getUTCHours(),2)+":"+T(this.getUTCMinutes(),2)+":"+T(this.getUTCSeconds(),2)+"."+T(this.getUTCMilliseconds(),3)+"Z"}})})();
"use strict";function db(a){a=q(a);return function(b){return a.test(b)}}
function eb(a){var b=a.getTime();return function(a){return!(!a||!a.getTime)&&a.getTime()===b}}function fb(a){return function(b,c,d){return b===a||a.call(this,b,c,d)}}function gb(a){return function(b,c,d){return b===a||a.call(d,c,b,d)}}function hb(a,b){var c={};return function(d,e,g){var f;if(!G(d))return!1;for(f in a)if(c[f]=c[f]||ib(a[f],b),!1===c[f].call(g,d[f],e,g))return!1;return!0}}function jb(a){return function(b){return b===a||Ua(b,a)}}
function ib(a,b){if(!ua(a)){if(D(a))return db(a);if(C(a))return eb(a);if(F(a))return b?gb(a):fb(a);if(va(a))return hb(a,b)}return jb(a)}function kb(a,b,c,d){return b?b.apply?b.apply(c,d||[]):F(a[b])?a[b].call(a):a[b]:a}function V(a,b,c,d){var e=+a.length;0>c&&(c=a.length+c);c=isNaN(c)?0:c;for(!0===d&&(e+=c);c<e;){d=c%a.length;if(!(d in a)){lb(a,b,c);break}if(!1===b.call(a,a[d],d,a))break;c++}}
function lb(a,b,c){var d=[],e;for(e in a)e in a&&(e>>>0==e&&4294967295!=e)&&e>=c&&d.push(parseInt(e));d.sort().each(function(c){return b.call(a,a[c],c,a)})}function mb(a,b,c,d,e,g){var f,h,l;0<a.length&&(l=ib(b),V(a,function(b,c){if(l.call(g,b,c,a))return f=b,h=c,!1},c,d));return e?h:f}function nb(a,b){var c=[],d={},e;V(a,function(g,f){e=b?kb(g,b,a,[g,f,a]):g;ob(d,e)||c.push(g)});return c}
function pb(a,b,c){var d=[],e={};b.each(function(a){ob(e,a)});a.each(function(a){var b=Ta(a),h=!Va(a);if(qb(e,b,a,h)!==c){var l=0;if(h)for(b=e[b];l<b.length;)b[l]===a?b.splice(l,1):l+=1;else delete e[b];d.push(a)}});return d}function rb(a,b,c){b=b||Infinity;c=c||0;var d=[];V(a,function(a){A(a)&&c<b?d=d.concat(rb(a,b,c+1)):d.push(a)});return d}function sb(a){var b=[];L(a,function(a){b=b.concat(a)});return b}function qb(a,b,c,d){var e=b in a;d&&(a[b]||(a[b]=[]),e=-1!==a[b].indexOf(c));return e}
function ob(a,b){var c=Ta(b),d=!Va(b),e=qb(a,c,b,d);d?a[c].push(b):a[c]=b;return e}function tb(a,b,c,d){var e,g,f,h=[],l="max"===c,n="min"===c,x=p.isArray(a);for(e in a)if(a.hasOwnProperty(e)){c=a[e];f=kb(c,b,a,x?[c,parseInt(e),a]:[]);if(N(f))throw new TypeError("Cannot compare with undefined");if(f===g)h.push(c);else if(N(g)||l&&f>g||n&&f<g)h=[c],g=f}x||(h=rb(h,1));return d?h:h[0]}
function ub(a,b){var c,d,e,g,f=0,h=0;c=p[xb];d=p[yb];var l=p[zb],n=p[Ab],x=p[Bb];a=Cb(a,c,d);b=Cb(b,c,d);do c=a.charAt(f),e=l[c]||c,c=b.charAt(f),g=l[c]||c,c=e?n.indexOf(e):null,d=g?n.indexOf(g):null,-1===c||-1===d?(c=a.charCodeAt(f)||null,d=b.charCodeAt(f)||null,x&&((c>=Ea&&c<=Fa||c>=Ga&&c<=Ha)&&(d>=Ea&&d<=Fa||d>=Ga&&d<=Ha))&&(c=Oa(a.slice(f)),d=Oa(b.slice(f)))):(e=e!==a.charAt(f),g=g!==b.charAt(f),e!==g&&0===h&&(h=e-g)),f+=1;while(null!=c&&null!=d&&c===d);return c===d?h:c-d}
function Cb(a,b,c){z(a)||(a=s(a));c&&(a=a.toLowerCase());b&&(a=a.replace(b,""));return a}var Ab="AlphanumericSortOrder",xb="AlphanumericSortIgnore",yb="AlphanumericSortIgnoreCase",zb="AlphanumericSortEquivalents",Bb="AlphanumericSortNatural";H(p,!1,!0,{create:function(){var a=[];L(arguments,function(b){if(!ua(b)&&"length"in b&&("[object Arguments]"===v.call(b)||b.callee)||!ua(b)&&"length"in b&&!z(b)&&!va(b))b=p.prototype.slice.call(b,0);a=a.concat(b)});return a}});
H(p,!0,!1,{find:function(a,b){ta(a);return mb(this,a,0,!1,!1,b)},findIndex:function(a,b){var c;ta(a);c=mb(this,a,0,!1,!0,b);return N(c)?-1:c}});
H(p,!0,!0,{findFrom:function(a,b,c){return mb(this,a,b,c)},findIndexFrom:function(a,b,c){b=mb(this,a,b,c,!0);return N(b)?-1:b},findAll:function(a,b,c){var d=[],e;0<this.length&&(e=ib(a),V(this,function(a,b,c){e(a,b,c)&&d.push(a)},b,c));return d},count:function(a){return N(a)?this.length:this.findAll(a).length},removeAt:function(a,b){if(N(a))return this;N(b)&&(b=a);this.splice(a,b-a+1);return this},include:function(a,b){return this.clone().add(a,b)},exclude:function(){return p.prototype.remove.apply(this.clone(),
arguments)},clone:function(){return xa([],this)},unique:function(a){return nb(this,a)},flatten:function(a){return rb(this,a)},union:function(){return nb(this.concat(sb(arguments)))},intersect:function(){return pb(this,sb(arguments),!1)},subtract:function(a){return pb(this,sb(arguments),!0)},at:function(){return Wa(this,arguments)},first:function(a){if(N(a))return this[0];0>a&&(a=0);return this.slice(0,a)},last:function(a){return N(a)?this[this.length-1]:this.slice(0>this.length-a?0:this.length-a)},
from:function(a){return this.slice(a)},to:function(a){N(a)&&(a=this.length);return this.slice(0,a)},min:function(a,b){return tb(this,a,"min",b)},max:function(a,b){return tb(this,a,"max",b)},least:function(a,b){return tb(this.groupBy.apply(this,[a]),"length","min",b)},most:function(a,b){return tb(this.groupBy.apply(this,[a]),"length","max",b)},sum:function(a){a=a?this.map(a):this;return 0<a.length?a.reduce(function(a,c){return a+c}):0},average:function(a){a=a?this.map(a):this;return 0<a.length?a.sum()/
a.length:0},inGroups:function(a,b){var c=1<arguments.length,d=this,e=[],g=Aa(this.length/a);wa(a,function(a){a*=g;var h=d.slice(a,a+g);c&&h.length<g&&wa(g-h.length,function(){h=h.add(b)});e.push(h)});return e},inGroupsOf:function(a,b){var c=[],d=this.length,e=this,g;if(0===d||0===a)return e;N(a)&&(a=1);N(b)&&(b=null);wa(Aa(d/a),function(d){for(g=e.slice(a*d,a*d+a);g.length<a;)g.push(b);c.push(g)});return c},isEmpty:function(){return 0==this.compact().length},sortBy:function(a,b){var c=this.clone();
c.sort(function(d,e){var g,f;g=kb(d,a,c,[d]);f=kb(e,a,c,[e]);return(z(g)&&z(f)?ub(g,f):g<f?-1:g>f?1:0)*(b?-1:1)});return c},randomize:function(){for(var a=this.concat(),b=a.length,c,d;b;)c=u.random()*b|0,d=a[--b],a[b]=a[c],a[c]=d;return a},zip:function(){var a=L(arguments);return this.map(function(b,c){return[b].concat(a.map(function(a){return c in a?a[c]:null}))})},sample:function(a){var b=this.randomize();return 0<arguments.length?b.slice(0,a):b[0]},each:function(a,b,c){V(this,a,b,c);return this},
add:function(a,b){if(!y(t(b))||isNaN(b))b=this.length;p.prototype.splice.apply(this,[b,0].concat(a));return this},remove:function(){var a=this;L(arguments,function(b){var c=0;for(b=ib(b);c<a.length;)b(a[c],c,a)?a.splice(c,1):c++});return a},compact:function(a){var b=[];V(this,function(c){A(c)?b.push(c.compact()):a&&c?b.push(c):a||(null==c||c.valueOf()!==c.valueOf())||b.push(c)});return b},groupBy:function(a,b){var c=this,d={},e;V(c,function(b,f){e=kb(b,a,c,[b,f,c]);d[e]||(d[e]=[]);d[e].push(b)});
b&&I(d,b);return d},none:function(){return!this.any.apply(this,arguments)}});H(p,!0,!0,{all:p.prototype.every,any:p.prototype.some,insert:p.prototype.add});function Db(a,b){K(m,!1,!0,a,function(a,d){a[d]=function(a,c,f){var h=m.keys(ya(a)),l;b||(l=ib(c,!0));f=p.prototype[d].call(h,function(d){var f=a[d];return b?kb(f,c,a,[d,f,a]):l(f,d,a)},f);A(f)&&(f=f.reduce(function(b,c){b[c]=a[c];return b},{}));return f}});Ya(a,O)}
H(m,!1,!0,{map:function(a,b){var c={},d,e;for(d in a)J(a,d)&&(e=a[d],c[d]=kb(e,b,a,[d,e,a]));return c},reduce:function(a){var b=m.keys(ya(a)).map(function(b){return a[b]});return b.reduce.apply(b,L(arguments,null,1))},each:function(a,b){ta(b);I(a,b);return a},size:function(a){return m.keys(ya(a)).length}});var Eb="any all none count find findAll isEmpty".split(" "),Fb="sum average min max least most".split(" "),Gb=["map","reduce","size"],Hb=Eb.concat(Fb).concat(Gb);
(function(){function a(){var a=arguments;return 0<a.length&&!F(a[0])}var b=p.prototype.map;K(p,!0,a,"every,all,some,filter,any,none,find,findIndex",function(a,b){var e=p.prototype[b];a[b]=function(a){var b=ib(a);return e.call(this,function(a,c){return b(a,c,this)})}});H(p,!0,a,{map:function(a){return b.call(this,function(b,e){return kb(b,a,this,[b,e,this])})}})})();
(function(){p[Ab]="A\u00c1\u00c0\u00c2\u00c3\u0104BC\u0106\u010c\u00c7D\u010e\u00d0E\u00c9\u00c8\u011a\u00ca\u00cb\u0118FG\u011eH\u0131I\u00cd\u00cc\u0130\u00ce\u00cfJKL\u0141MN\u0143\u0147\u00d1O\u00d3\u00d2\u00d4PQR\u0158S\u015a\u0160\u015eT\u0164U\u00da\u00d9\u016e\u00db\u00dcVWXY\u00ddZ\u0179\u017b\u017d\u00de\u00c6\u0152\u00d8\u00d5\u00c5\u00c4\u00d6".split("").map(function(a){return a+a.toLowerCase()}).join("");var a={};V("A\u00c1\u00c0\u00c2\u00c3\u00c4 C\u00c7 E\u00c9\u00c8\u00ca\u00cb I\u00cd\u00cc\u0130\u00ce\u00cf O\u00d3\u00d2\u00d4\u00d5\u00d6 S\u00df U\u00da\u00d9\u00db\u00dc".split(" "),
function(b){var c=b.charAt(0);V(b.slice(1).split(""),function(b){a[b]=c;a[b.toLowerCase()]=c.toLowerCase()})});p[Bb]=!0;p[yb]=!0;p[zb]=a})();Db(Eb);Db(Fb,!0);Ya(Gb,O);p.AlphanumericSort=ub;
"use strict";
var W,Ib,Jb="ampm hour minute second ampm utc offset_sign offset_hours offset_minutes ampm".split(" "),Kb="({t})?\\s*(\\d{1,2}(?:[,.]\\d+)?)(?:{h}([0-5]\\d(?:[,.]\\d+)?)?{m}(?::?([0-5]\\d(?:[,.]\\d+)?){s})?\\s*(?:({t})|(Z)|(?:([+-])(\\d{2,2})(?::?(\\d{2,2}))?)?)?|\\s*({t}))",Lb={},Mb,Nb,Ob,Pb=[],Qb={},X={yyyy:function(a){return U(a,"FullYear")},yy:function(a){return U(a,"FullYear")%100},ord:function(a){a=U(a,"Date");return a+Pa(a)},tz:function(a){return a.getUTCOffset()},isotz:function(a){return a.getUTCOffset(!0)},
Z:function(a){return a.getUTCOffset()},ZZ:function(a){return a.getUTCOffset().replace(/(\d{2})$/,":$1")}},Rb=[{name:"year",method:"FullYear",k:!0,b:function(a){return 864E5*(365+(a?a.isLeapYear()?1:0:0.25))}},{name:"month",error:0.919,method:"Month",k:!0,b:function(a,b){var c=30.4375,d;a&&(d=a.daysInMonth(),b<=d.days()&&(c=d));return 864E5*c}},{name:"week",method:"ISOWeek",b:aa(6048E5)},{name:"day",error:0.958,method:"Date",k:!0,b:aa(864E5)},{name:"hour",method:"Hours",b:aa(36E5)},{name:"minute",
method:"Minutes",b:aa(6E4)},{name:"second",method:"Seconds",b:aa(1E3)},{name:"millisecond",method:"Milliseconds",b:aa(1)}],Sb={};function Tb(a){xa(this,a);this.g=Pb.concat()}
Tb.prototype={getMonth:function(a){return y(a)?a-1:this.months.indexOf(a)%12},getWeekday:function(a){return this.weekdays.indexOf(a)%7},addFormat:function(a,b,c,d,e){var g=c||[],f=this,h;a=a.replace(/\s+/g,"[,. ]*");a=a.replace(/\{([^,]+?)\}/g,function(a,b){var d,e,h,B=b.match(/\?$/);h=b.match(/^(\d+)\??$/);var k=b.match(/(\d)(?:-(\d))?/),E=b.replace(/[^a-z]+$/,"");h?d=f.tokens[h[1]]:f[E]?d=f[E]:f[E+"s"]&&(d=f[E+"s"],k&&(e=[],d.forEach(function(a,b){var c=b%(f.units?8:d.length);c>=k[1]&&c<=(k[2]||
k[1])&&e.push(a)}),d=e),d=Ub(d));h?h="(?:"+d+")":(c||g.push(E),h="("+d+")");B&&(h+="?");return h});b?(b=Vb(f,e),e=["t","[\\s\\u3000]"].concat(f.timeMarker),h=a.match(/\\d\{\d,\d\}\)+\??$/),Wb(f,"(?:"+b+")[,\\s\\u3000]+?"+a,Jb.concat(g),d),Wb(f,a+"(?:[,\\s]*(?:"+e.join("|")+(h?"+":"*")+")"+b+")?",g.concat(Jb),d)):Wb(f,a,g,d)}};
function Xb(a,b,c){var d,e,g=b[0],f=b[1],h=b[2];b=a[c]||a.relative;if(F(b))return b.call(a,g,f,h,c);e=a.units[8*(a.plural&&1<g?1:0)+f]||a.units[f];a.capitalizeUnit&&(e=Yb(e));d=a.modifiers.filter(function(a){return"sign"==a.name&&a.value==(0<h?1:-1)})[0];return b.replace(/\{(.*?)\}/g,function(a,b){switch(b){case "num":return g;case "unit":return e;case "sign":return d.src}})}function Zb(a,b){b=b||a.code;return"en"===b||"en-US"===b?!0:a.variant}
function $b(a,b){return b.replace(q(a.num,"g"),function(b){return ac(a,b)||""})}function ac(a,b){var c;return y(b)?b:b&&-1!==(c=a.numbers.indexOf(b))?(c+1)%10:1}function Y(a,b){var c;z(a)||(a="");c=Sb[a]||Sb[a.slice(0,2)];if(!1===b&&!c)throw new TypeError("Invalid locale.");return c||Ib}
function bc(a,b){function c(a){var b=h[a];z(b)?h[a]=b.split(","):b||(h[a]=[])}function d(a,b){a=a.split("+").map(function(a){return a.replace(/(.+):(.+)$/,function(a,b,c){return c.split("|").map(function(a){return b+a}).join("|")})}).join("|");a.split("|").forEach(b)}function e(a,b,c){var e=[];h[a].forEach(function(a,f){b&&(a+="+"+a.slice(0,3));d(a,function(a,b){e[b*c+f]=a.toLowerCase()})});h[a]=e}function g(a,b,c){a="\\d{"+a+","+b+"}";c&&(a+="|(?:"+Ub(h.numbers)+")+");return a}function f(a,b){h[a]=
h[a]||b}var h,l;h=new Tb(b);c("modifiers");"months weekdays units numbers articles tokens timeMarker ampm timeSuffixes dateParse timeParse".split(" ").forEach(c);l=!h.monthSuffix;e("months",l,12);e("weekdays",l,7);e("units",!1,8);e("numbers",!1,10);f("code",a);f("date",g(1,2,h.digitDate));f("year","'\\d{2}|"+g(4,4));f("num",function(){var a=["-?\\d+"].concat(h.articles);h.numbers&&(a=a.concat(h.numbers));return Ub(a)}());(function(){var a=[];h.i={};h.modifiers.push({name:"day",src:"yesterday",value:-1});
h.modifiers.push({name:"day",src:"today",value:0});h.modifiers.push({name:"day",src:"tomorrow",value:1});h.modifiers.forEach(function(b){var c=b.name;d(b.src,function(d){var e=h[c];h.i[d]=b;a.push({name:c,src:d,value:b.value});h[c]=e?e+"|"+d:d})});h.day+="|"+Ub(h.weekdays);h.modifiers=a})();h.monthSuffix&&(h.month=g(1,2),h.months="1 2 3 4 5 6 7 8 9 10 11 12".split(" ").map(function(a){return a+h.monthSuffix}));h.full_month=g(1,2)+"|"+Ub(h.months);0<h.timeSuffixes.length&&h.addFormat(Vb(h),!1,Jb);
h.addFormat("{day}",!0);h.addFormat("{month}"+(h.monthSuffix||""));h.addFormat("{year}"+(h.yearSuffix||""));h.timeParse.forEach(function(a){h.addFormat(a,!0)});h.dateParse.forEach(function(a){h.addFormat(a)});return Sb[a]=h}function Wb(a,b,c,d){a.g.unshift({r:d,locale:a,q:q("^"+b+"$","i"),to:c})}function Yb(a){return a.slice(0,1).toUpperCase()+a.slice(1)}function Ub(a){return a.filter(function(a){return!!a}).join("|")}function cc(){var a=r.SugarNewDate;return a?a():new r}
function dc(a,b){var c;if(G(a[0]))return a;if(y(a[0])&&!y(a[1]))return[a[0]];if(z(a[0])&&b)return[ec(a[0]),a[1]];c={};Nb.forEach(function(b,e){c[b.name]=a[e]});return[c]}function ec(a){var b,c={};if(a=a.match(/^(\d+)?\s?(\w+?)s?$/i))N(b)&&(b=parseInt(a[1])||1),c[a[2].toLowerCase()]=b;return c}function fc(a,b,c){var d;N(c)&&(c=Ob.length);for(b=b||0;b<c&&(d=Ob[b],!1!==a(d.name,d,b));b++);}
function gc(a,b){var c={},d,e;b.forEach(function(b,f){d=a[f+1];N(d)||""===d||("year"===b&&(c.t=d.replace(/'/,"")),e=parseFloat(d.replace(/'/,"").replace(/,/,".")),c[b]=isNaN(e)?d.toLowerCase():e)});return c}function hc(a){a=a.trim().replace(/^just (?=now)|\.+$/i,"");return ic(a)}
function ic(a){return a.replace(Mb,function(a,c,d){var e=0,g=1,f,h;if(c)return a;d.split("").reverse().forEach(function(a){a=Lb[a];var b=9<a;b?(f&&(e+=g),g*=a/(h||1),h=a):(!1===f&&(g*=10),e+=g*a);f=b});f&&(e+=g);return e})}
function jc(a,b,c,d){function e(a){vb.push(a)}function g(){vb.forEach(function(a){a.call()})}function f(){var a=n.getWeekday();n.setWeekday(7*(k.num-1)+(a>Ba?Ba+7:Ba))}function h(){var a=B.i[k.edge];fc(function(a){if(M(k[a]))return E=a,!1},4);if("year"===E)k.e="month";else if("month"===E||"week"===E)k.e="day";n[(0>a.value?"endOf":"beginningOf")+Yb(E)]();-2===a.value&&n.reset()}function l(){var a;fc(function(b,c,d){"day"===b&&(b="date");if(M(k[b])){if(d>=wb)return n.setTime(NaN),!1;a=a||{};a[b]=k[b];
delete k[b]}});a&&e(function(){n.set(a,!0)})}var n,x,ha,vb,B,k,E,wb,Ba,ra,ca;n=cc();vb=[];n.utc(d);C(a)?n.utc(a.isUTC()).setTime(a.getTime()):y(a)?n.setTime(a):G(a)?(n.set(a,!0),k=a):z(a)&&(ha=Y(b),a=hc(a),ha&&I(ha.o?[ha.o].concat(ha.g):ha.g,function(c,d){var g=a.match(d.q);if(g){B=d.locale;k=gc(g,d.to);B.o=d;k.utc&&n.utc();if(k.timestamp)return k=k.timestamp,!1;d.r&&(!z(k.month)&&(z(k.date)||Zb(ha,b)))&&(ca=k.month,k.month=k.date,k.date=ca);k.year&&2===k.t.length&&(k.year=100*R(U(cc(),"FullYear")/
100)-100*R(k.year/100)+k.year);k.month&&(k.month=B.getMonth(k.month),k.shift&&!k.unit&&(k.unit=B.units[7]));k.weekday&&k.date?delete k.weekday:k.weekday&&(k.weekday=B.getWeekday(k.weekday),k.shift&&!k.unit&&(k.unit=B.units[5]));k.day&&(ca=B.i[k.day])?(k.day=ca.value,n.reset(),x=!0):k.day&&-1<(Ba=B.getWeekday(k.day))&&(delete k.day,k.num&&k.month?(e(f),k.day=1):k.weekday=Ba);k.date&&!y(k.date)&&(k.date=$b(B,k.date));k.ampm&&k.ampm===B.ampm[1]&&12>k.hour?k.hour+=12:k.ampm===B.ampm[0]&&12===k.hour&&
(k.hour=0);if("offset_hours"in k||"offset_minutes"in k)n.utc(),k.offset_minutes=k.offset_minutes||0,k.offset_minutes+=60*k.offset_hours,"-"===k.offset_sign&&(k.offset_minutes*=-1),k.minute-=k.offset_minutes;k.unit&&(x=!0,ra=ac(B,k.num),wb=B.units.indexOf(k.unit)%8,E=W.units[wb],l(),k.shift&&(ra*=(ca=B.i[k.shift])?ca.value:0),k.sign&&(ca=B.i[k.sign])&&(ra*=ca.value),M(k.weekday)&&(n.set({weekday:k.weekday},!0),delete k.weekday),k[E]=(k[E]||0)+ra);k.edge&&e(h);"-"===k.year_sign&&(k.year*=-1);fc(function(a,
b,c){b=k[a];var d=b%1;d&&(k[Ob[c-1].name]=R(d*("second"===a?1E3:60)),k[a]=Q(b))},1,4);return!1}}),k?x?n.advance(k):(n._utc&&n.reset(),kc(n,k,!0,!1,c)):("now"!==a&&(n=new r(a)),d&&n.addMinutes(-n.getTimezoneOffset())),g(),n.utc(!1));return{c:n,set:k}}function lc(a){var b,c=P(a),d=c,e=0;fc(function(a,f,h){b=Q(Da(c/f.b(),1));1<=b&&(d=b,e=h)},1);return[d,e,a]}
function mc(a){var b=lc(a.millisecondsFromNow());if(6===b[1]||5===b[1]&&4===b[0]&&a.daysFromNow()>=cc().daysInMonth())b[0]=P(a.monthsFromNow()),b[1]=6;return b}function nc(a,b,c){function d(a,c){var d=U(a,"Month");return Y(c).months[d+12*b]}Z(a,d,c);Z(Yb(a),d,c,1)}function Z(a,b,c,d){X[a]=function(a,g){var f=b(a,g);c&&(f=f.slice(0,c));d&&(f=f.slice(0,d).toUpperCase()+f.slice(d));return f}}
function oc(a,b,c){X[a]=b;X[a+a]=function(a,c){return T(b(a,c),2)};c&&(X[a+a+a]=function(a,c){return T(b(a,c),3)},X[a+a+a+a]=function(a,c){return T(b(a,c),4)})}function pc(a){var b=a.match(/(\{\w+\})|[^{}]+/g);Qb[a]=b.map(function(a){a.replace(/\{(\w+)\}/,function(b,e){a=X[e]||e;return e});return a})}
function qc(a,b,c,d){var e;if(!a.isValid())return"Invalid Date";Date[b]?b=Date[b]:F(b)&&(e=mc(a),b=b.apply(a,e.concat(Y(d))));if(!b&&c)return e=e||mc(a),0===e[1]&&(e[1]=1,e[0]=1),a=Y(d),Xb(a,e,0<e[2]?"future":"past");b=b||"long";if("short"===b||"long"===b||"full"===b)b=Y(d)[b];Qb[b]||pc(b);var g,f;e="";b=Qb[b];g=0;for(c=b.length;g<c;g++)f=b[g],e+=F(f)?f(a,d):f;return e}
function rc(a,b,c,d,e){var g,f,h,l=0,n=0,x=0;g=jc(b,c,null,e);0<d&&(n=x=d,f=!0);if(!g.c.isValid())return!1;if(g.set&&g.set.e){Rb.forEach(function(b){b.name===g.set.e&&(l=b.b(g.c,a-g.c)-1)});b=Yb(g.set.e);if(g.set.edge||g.set.shift)g.c["beginningOf"+b]();"month"===g.set.e&&(h=g.c.clone()["endOf"+b]().getTime());!f&&(g.set.sign&&"millisecond"!=g.set.e)&&(n=50,x=-50)}f=a.getTime();b=g.c.getTime();h=sc(a,b,h||b+l);return f>=b-n&&f<=h+x}
function sc(a,b,c){b=new r(b);a=(new r(c)).utc(a.isUTC());23!==U(a,"Hours")&&(b=b.getTimezoneOffset(),a=a.getTimezoneOffset(),b!==a&&(c+=(a-b).minutes()));return c}
function kc(a,b,c,d,e){function g(a){return M(b[a])?b[a]:b[a+"s"]}function f(a){return M(g(a))}var h;if(y(b)&&d)b={milliseconds:b};else if(y(b))return a.setTime(b),a;M(b.date)&&(b.day=b.date);fc(function(d,e,g){var l="day"===d;if(f(d)||l&&f("weekday"))return b.e=d,h=+g,!1;!c||("week"===d||l&&f("week"))||Sa(a,e.method,l?1:0)});Rb.forEach(function(c){var e=c.name;c=c.method;var h;h=g(e);N(h)||(d?("week"===e&&(h=(b.day||0)+7*h,c="Date"),h=h*d+U(a,c)):"month"===e&&f("day")&&Sa(a,"Date",15),Sa(a,c,h),
d&&"month"===e&&(e=h,0>e&&(e=e%12+12),e%12!=U(a,"Month")&&Sa(a,"Date",0)))});d||(f("day")||!f("weekday"))||a.setWeekday(g("weekday"));var l;a:{switch(e){case -1:l=a>cc();break a;case 1:l=a<cc();break a}l=void 0}l&&fc(function(b,c){if((c.k||"week"===b&&f("weekday"))&&!(f(b)||"day"===b&&f("weekday")))return a[c.j](e),!1},h+1);return a}
function Vb(a,b){var c=Kb,d={h:0,m:1,s:2},e;a=a||W;return c.replace(/{([a-z])}/g,function(c,f){var h=[],l="h"===f,n=l&&!b;if("t"===f)return a.ampm.join("|");l&&h.push(":");(e=a.timeSuffixes[d[f]])&&h.push(e+"\\s*");return 0===h.length?"":"(?:"+h.join("|")+")"+(n?"":"?")})}function tc(a,b,c){var d,e;y(a[1])?d=dc(a)[0]:(d=a[0],e=a[1]);return jc(d,e,b,c).c}
H(r,!1,!0,{create:function(){return tc(arguments)},past:function(){return tc(arguments,-1)},future:function(){return tc(arguments,1)},addLocale:function(a,b){return bc(a,b)},setLocale:function(a){var b=Y(a,!1);Ib=b;a&&a!=b.code&&(b.code=a);return b},getLocale:function(a){return a?Y(a,!1):Ib},addFormat:function(a,b,c){Wb(Y(c),a,b)}});
H(r,!0,!0,{set:function(){var a=dc(arguments);return kc(this,a[0],a[1])},setWeekday:function(a){if(!N(a))return Sa(this,"Date",U(this,"Date")+a-U(this,"Day"))},setISOWeek:function(a){var b=U(this,"Day")||7;if(!N(a))return this.set({month:0,date:4}),this.set({weekday:1}),1<a&&this.addWeeks(a-1),1!==b&&this.advance({days:b-1}),this.getTime()},getISOWeek:function(){var a;a=this.clone();var b=U(a,"Day")||7;a.addDays(4-b).reset();return 1+Q(a.daysSince(a.clone().beginningOfYear())/7)},beginningOfISOWeek:function(){var a=
this.getDay();0===a?a=-6:1!==a&&(a=1);this.setWeekday(a);return this.reset()},endOfISOWeek:function(){0!==this.getDay()&&this.setWeekday(7);return this.endOfDay()},getUTCOffset:function(a){var b=this._utc?0:this.getTimezoneOffset(),c=!0===a?":":"";return!b&&a?"Z":T(Q(-b/60),2,!0)+c+T(P(b%60),2)},utc:function(a){oa(this,"_utc",!0===a||0===arguments.length);return this},isUTC:function(){return!!this._utc||0===this.getTimezoneOffset()},advance:function(){var a=dc(arguments,!0);return kc(this,a[0],a[1],
1)},rewind:function(){var a=dc(arguments,!0);return kc(this,a[0],a[1],-1)},isValid:function(){return!isNaN(this.getTime())},isAfter:function(a,b){return this.getTime()>r.create(a).getTime()-(b||0)},isBefore:function(a,b){return this.getTime()<r.create(a).getTime()+(b||0)},isBetween:function(a,b,c){var d=this.getTime();a=r.create(a).getTime();var e=r.create(b).getTime();b=Ca(a,e);a=S(a,e);c=c||0;return b-c<d&&a+c>d},isLeapYear:function(){var a=U(this,"FullYear");return 0===a%4&&0!==a%100||0===a%400},
daysInMonth:function(){return 32-U(new r(U(this,"FullYear"),U(this,"Month"),32),"Date")},format:function(a,b){return qc(this,a,!1,b)},relative:function(a,b){z(a)&&(b=a,a=null);return qc(this,a,!0,b)},is:function(a,b,c){var d,e;if(this.isValid()){if(z(a))switch(a=a.trim().toLowerCase(),e=this.clone().utc(c),!0){case "future"===a:return this.getTime()>cc().getTime();case "past"===a:return this.getTime()<cc().getTime();case "weekday"===a:return 0<U(e,"Day")&&6>U(e,"Day");case "weekend"===a:return 0===
U(e,"Day")||6===U(e,"Day");case -1<(d=W.weekdays.indexOf(a)%7):return U(e,"Day")===d;case -1<(d=W.months.indexOf(a)%12):return U(e,"Month")===d}return rc(this,a,null,b,c)}},reset:function(a){var b={},c;a=a||"hours";"date"===a&&(a="days");c=Rb.some(function(b){return a===b.name||a===b.name+"s"});b[a]=a.match(/^days?/)?1:0;return c?this.set(b,!0):this},clone:function(){var a=new r(this.getTime());a.utc(!!this._utc);return a}});
H(r,!0,!0,{iso:function(){return this.toISOString()},getWeekday:r.prototype.getDay,getUTCWeekday:r.prototype.getUTCDay});function uc(a,b){function c(){return R(this*b)}function d(){return tc(arguments)[a.j](this)}function e(){return tc(arguments)[a.j](-this)}var g=a.name,f={};f[g]=c;f[g+"s"]=c;f[g+"Before"]=e;f[g+"sBefore"]=e;f[g+"Ago"]=e;f[g+"sAgo"]=e;f[g+"After"]=d;f[g+"sAfter"]=d;f[g+"FromNow"]=d;f[g+"sFromNow"]=d;t.extend(f)}H(t,!0,!0,{duration:function(a){a=Y(a);return Xb(a,lc(this),"duration")}});
W=Ib=r.addLocale("en",{plural:!0,timeMarker:"at",ampm:"am,pm",months:"January,February,March,April,May,June,July,August,September,October,November,December",weekdays:"Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday",units:"millisecond:|s,second:|s,minute:|s,hour:|s,day:|s,week:|s,month:|s,year:|s",numbers:"one,two,three,four,five,six,seven,eight,nine,ten",articles:"a,an,the",tokens:"the,st|nd|rd|th,of","short":"{Month} {d}, {yyyy}","long":"{Month} {d}, {yyyy} {h}:{mm}{tt}",full:"{Weekday} {Month} {d}, {yyyy} {h}:{mm}:{ss}{tt}",
past:"{num} {unit} {sign}",future:"{num} {unit} {sign}",duration:"{num} {unit}",modifiers:[{name:"sign",src:"ago|before",value:-1},{name:"sign",src:"from now|after|from|in|later",value:1},{name:"edge",src:"last day",value:-2},{name:"edge",src:"end",value:-1},{name:"edge",src:"first day|beginning",value:1},{name:"shift",src:"last",value:-1},{name:"shift",src:"the|this",value:0},{name:"shift",src:"next",value:1}],dateParse:["{month} {year}","{shift} {unit=5-7}","{0?} {date}{1}","{0?} {edge} of {shift?} {unit=4-7?}{month?}{year?}"],
timeParse:"{num} {unit} {sign};{sign} {num} {unit};{0} {num}{1} {day} of {month} {year?};{weekday?} {month} {date}{1?} {year?};{date} {month} {year};{date} {month};{shift} {weekday};{shift} week {weekday};{weekday} {2?} {shift} week;{num} {unit=4-5} {sign} {day};{0?} {date}{1} of {month};{0?}{month?} {date?}{1?} of {shift} {unit=6-7}".split(";")});Ob=Rb.concat().reverse();Nb=Rb.concat();Nb.splice(2,1);
K(r,!0,!0,Rb,function(a,b,c){function d(a){a/=f;var c=a%1,d=b.error||0.999;c&&P(c%1)>d&&(a=R(a));return 0>a?Aa(a):Q(a)}var e=b.name,g=Yb(e),f=b.b(),h,l;b.j="add"+g+"s";h=function(a,b){return d(this.getTime()-r.create(a,b).getTime())};l=function(a,b){return d(r.create(a,b).getTime()-this.getTime())};a[e+"sAgo"]=l;a[e+"sUntil"]=l;a[e+"sSince"]=h;a[e+"sFromNow"]=h;a[b.j]=function(a,b){var c={};c[e]=a;return this.advance(c,b)};uc(b,f);3>c&&["Last","This","Next"].forEach(function(b){a["is"+b+g]=function(){return rc(this,
b+" "+e,"en")}});4>c&&(a["beginningOf"+g]=function(){var a={};switch(e){case "year":a.year=U(this,"FullYear");break;case "month":a.month=U(this,"Month");break;case "day":a.day=U(this,"Date");break;case "week":a.weekday=0}return this.set(a,!0)},a["endOf"+g]=function(){var a={hours:23,minutes:59,seconds:59,milliseconds:999};switch(e){case "year":a.month=11;a.day=31;break;case "month":a.day=this.daysInMonth();break;case "week":a.weekday=6}return this.set(a,!0)})});
W.addFormat("([+-])?(\\d{4,4})[-.]?{full_month}[-.]?(\\d{1,2})?",!0,["year_sign","year","month","date"],!1,!0);W.addFormat("(\\d{1,2})[-.\\/]{full_month}(?:[-.\\/](\\d{2,4}))?",!0,["date","month","year"],!0);W.addFormat("{full_month}[-.](\\d{4,4})",!1,["month","year"]);W.addFormat("\\/Date\\((\\d+(?:[+-]\\d{4,4})?)\\)\\/",!1,["timestamp"]);W.addFormat(Vb(W),!1,Jb);Pb=W.g.slice(0,7).reverse();W.g=W.g.slice(7).concat(Pb);oc("f",function(a){return U(a,"Milliseconds")},!0);
oc("s",function(a){return U(a,"Seconds")});oc("m",function(a){return U(a,"Minutes")});oc("h",function(a){return U(a,"Hours")%12||12});oc("H",function(a){return U(a,"Hours")});oc("d",function(a){return U(a,"Date")});oc("M",function(a){return U(a,"Month")+1});(function(){function a(a,c){var d=U(a,"Hours");return Y(c).ampm[Q(d/12)]||""}Z("t",a,1);Z("tt",a);Z("T",a,1,1);Z("TT",a,null,2)})();
(function(){function a(a,c){var d=U(a,"Day");return Y(c).weekdays[d]}Z("dow",a,3);Z("Dow",a,3,1);Z("weekday",a);Z("Weekday",a,null,1)})();nc("mon",0,3);nc("month",0);nc("month2",1);nc("month3",2);X.ms=X.f;X.milliseconds=X.f;X.seconds=X.s;X.minutes=X.m;X.hours=X.h;X["24hr"]=X.H;X["12hr"]=X.h;X.date=X.d;X.day=X.d;X.year=X.yyyy;K(r,!0,!0,"short,long,full",function(a,b){a[b]=function(a){return qc(this,b,!1,a)}});
"\u3007\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07".split("").forEach(function(a,b){9<b&&(b=za(10,b-9));Lb[a]=b});xa(Lb,Ka);Mb=q("([\u671f\u9031\u5468])?([\u3007\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07"+Ja+"]+)(?!\u6628)","g");
(function(){var a=W.weekdays.slice(0,7),b=W.months.slice(0,12);K(r,!0,!0,"today yesterday tomorrow weekday weekend future past".split(" ").concat(a).concat(b),function(a,b){a["is"+Yb(b)]=function(a){return this.is(b,0,a)}})})();r.utc||(r.utc={create:function(){return tc(arguments,0,!0)},past:function(){return tc(arguments,-1,!0)},future:function(){return tc(arguments,1,!0)}});
H(r,!1,!0,{RFC1123:"{Dow}, {dd} {Mon} {yyyy} {HH}:{mm}:{ss} {tz}",RFC1036:"{Weekday}, {dd}-{Mon}-{yy} {HH}:{mm}:{ss} {tz}",ISO8601_DATE:"{yyyy}-{MM}-{dd}",ISO8601_DATETIME:"{yyyy}-{MM}-{dd}T{HH}:{mm}:{ss}.{fff}{isotz}"});
"use strict";function Range(a,b){this.start=vc(a);this.end=vc(b)}function vc(a){return C(a)?new r(a.getTime()):null==a?a:C(a)?a.getTime():a.valueOf()}function wc(a){a=null==a?a:C(a)?a.getTime():a.valueOf();return!!a||0===a}
function xc(a,b){var c,d,e,g;if(y(b))return new r(a.getTime()+b);c=b[0];d=b[1];e=U(a,d);g=new r(a.getTime());Sa(g,d,e+c);return g}function yc(a,b){return s.fromCharCode(a.charCodeAt(0)+b)}function zc(a,b){return a+b}Range.prototype.toString=function(){return this.isValid()?this.start+".."+this.end:"Invalid Range"};
H(Range,!0,!0,{isValid:function(){return wc(this.start)&&wc(this.end)&&typeof this.start===typeof this.end},span:function(){return this.isValid()?P((z(this.end)?this.end.charCodeAt(0):this.end)-(z(this.start)?this.start.charCodeAt(0):this.start))+1:NaN},contains:function(a){return null==a?!1:a.start&&a.end?a.start>=this.start&&a.start<=this.end&&a.end>=this.start&&a.end<=this.end:a>=this.start&&a<=this.end},every:function(a,b){var c,d=this.start,e=this.end,g=e<d,f=d,h=0,l=[];F(a)&&(b=a,a=null);a=
a||1;y(d)?c=zc:z(d)?c=yc:C(d)&&(c=a,y(c)?a=c:(d=c.toLowerCase().match(/^(\d+)?\s?(\w+?)s?$/i),c=parseInt(d[1])||1,d=d[2].slice(0,1).toUpperCase()+d[2].slice(1),d.match(/hour|minute|second/i)?d+="s":"Year"===d?d="FullYear":"Day"===d&&(d="Date"),a=[c,d]),c=xc);for(g&&0<a&&(a*=-1);g?f>=e:f<=e;)l.push(f),b&&b(f,h),f=c(f,a),h++;return l},union:function(a){return new Range(this.start<a.start?this.start:a.start,this.end>a.end?this.end:a.end)},intersect:function(a){return a.start>this.end||a.end<this.start?
new Range(NaN,NaN):new Range(this.start>a.start?this.start:a.start,this.end<a.end?this.end:a.end)},clone:function(){return new Range(this.start,this.end)},clamp:function(a){var b=this.start,c=this.end,d=c<b?c:b,b=b>c?b:c;return vc(a<d?d:a>b?b:a)}});[t,s,r].forEach(function(a){H(a,!1,!0,{range:function(b,c){a.create&&(b=a.create(b),c=a.create(c));return new Range(b,c)}})});
H(t,!0,!0,{upto:function(a,b,c){return t.range(this,a).every(c,b)},clamp:function(a,b){return(new Range(a,b)).clamp(this)},cap:function(a){return this.clamp(void 0,a)}});H(t,!0,!0,{downto:t.prototype.upto});H(p,!1,function(a){return a instanceof Range},{create:function(a){return a.every()}});
"use strict";function Ac(a,b,c,d,e){Infinity!==b&&(a.timers||(a.timers=[]),y(b)||(b=1),a.n=!1,a.timers.push(setTimeout(function(){a.n||c.apply(d,e||[])},b)))}
H(Function,!0,!0,{lazy:function(a,b,c){function d(){g.length<c-(f&&b?1:0)&&g.push([this,arguments]);f||(f=!0,b?h():Ac(d,l,h));return x}var e=this,g=[],f=!1,h,l,n,x;a=a||1;c=c||Infinity;l=Aa(a);n=R(l/a)||1;h=function(){var a=g.length,b;if(0!=a){for(b=S(a-n,0);a>b;)x=Function.prototype.apply.apply(e,g.shift()),a--;Ac(d,l,function(){f=!1;h()})}};return d},throttle:function(a){return this.lazy(a,!0,1)},debounce:function(a){function b(){b.cancel();Ac(b,a,c,this,arguments)}var c=this;return b},delay:function(a){var b=
L(arguments,null,1);Ac(this,a,this,this,b);return this},every:function(a){function b(){c.apply(c,d);Ac(c,a,b)}var c=this,d=arguments,d=1<d.length?L(d,null,1):[];Ac(c,a,b);return c},cancel:function(){var a=this.timers,b;if(A(a))for(;b=a.shift();)clearTimeout(b);this.n=!0;return this},after:function(a){var b=this,c=0,d=[];if(!y(a))a=1;else if(0===a)return b.call(),b;return function(){var e;d.push(L(arguments));c++;if(c==a)return e=b.call(this,d),c=0,d=[],e}},once:function(){return this.throttle(Infinity,
!0)},fill:function(){var a=this,b=L(arguments);return function(){var c=L(arguments);b.forEach(function(a,b){(null!=a||b>=c.length)&&c.splice(b,0,a)});return a.apply(this,c)}}});
"use strict";function Bc(a,b,c,d,e,g){var f=a.toFixed(20),h=f.search(/\./),f=f.search(/[1-9]/),h=h-f;0<h&&(h-=1);e=S(Ca(Q(h/3),!1===e?c.length:e),-d);d=c.charAt(e+d-1);-9>h&&(e=-3,b=P(h)-9,d=c.slice(0,1));c=g?za(2,10*e):za(10,3*e);return Da(a/c,b||0).format()+d.trim()}
H(t,!1,!0,{random:function(a,b){var c,d;1==arguments.length&&(b=a,a=0);c=Ca(a||0,N(b)?1:b);d=S(a||0,N(b)?1:b)+1;return Q(u.random()*(d-c)+c)}});
H(t,!0,!0,{log:function(a){return u.log(this)/(a?u.log(a):1)},abbr:function(a){return Bc(this,a,"kmbt",0,4)},metric:function(a,b){return Bc(this,a,"n\u03bcm kMGTPE",4,N(b)?1:b)},bytes:function(a,b){return Bc(this,a,"kMGTPE",0,N(b)?4:b,!0)+"B"},isInteger:function(){return 0==this%1},isOdd:function(){return!isNaN(this)&&!this.isMultipleOf(2)},isEven:function(){return this.isMultipleOf(2)},isMultipleOf:function(a){return 0===this%a},format:function(a,b,c){var d,e,g,f="";N(b)&&(b=",");N(c)&&(c=".");d=
(y(a)?Da(this,a||0).toFixed(S(a,0)):this.toString()).replace(/^-/,"").split(".");e=d[0];g=d[1];for(d=e.length;0<d;d-=3)d<e.length&&(f=b+f),f=e.slice(S(0,d-3),d)+f;g&&(f+=c+Na("0",(a||0)-g.length)+g);return(0>this?"-":"")+f},hex:function(a){return this.pad(a||1,!1,16)},times:function(a){if(a)for(var b=0;b<this;b++)a.call(this,b);return this.toNumber()},chr:function(){return s.fromCharCode(this)},pad:function(a,b,c){return T(this,a,b,c)},ordinalize:function(){var a=P(this),a=parseInt(a.toString().slice(-2));
return this+Pa(a)},toNumber:function(){return parseFloat(this,10)}});(function(){function a(a){return function(c){return c?Da(this,c,a):a(this)}}H(t,!0,!0,{ceil:a(Aa),round:a(R),floor:a(Q)});K(t,!0,!0,"abs,pow,sin,asin,cos,acos,tan,atan,exp,pow,sqrt",function(a,c){a[c]=function(a,b){return u[c](this,a,b)}})})();
"use strict";var Cc=["isObject","isNaN"],Dc="keys values select reject each merge clone equal watch tap has toQueryString".split(" ");
function Ec(a,b,c,d){var e,g,f;(g=b.match(/^(.+?)(\[.*\])$/))?(f=g[1],b=g[2].replace(/^\[|\]$/g,"").split("]["),b.forEach(function(b){e=!b||b.match(/^\d+$/);!f&&A(a)&&(f=a.length);J(a,f)||(a[f]=e?[]:{});a=a[f];f=b}),!f&&e&&(f=a.length.toString()),Ec(a,f,c,d)):a[b]=d&&"true"===c?!0:d&&"false"===c?!1:c}function Fc(a,b){var c;return A(b)||G(b)&&b.toString===v?(c=[],I(b,function(b,e){a&&(b=a+"["+b+"]");c.push(Fc(b,e))}),c.join("&")):a?Gc(a)+"="+(C(b)?b.getTime():Gc(b)):""}
function Gc(a){return a||!1===a||0===a?encodeURIComponent(a).replace(/%20/g,"+"):""}function Hc(a,b,c){var d,e=a instanceof O?new O:{};I(a,function(a,f){d=!1;sa(b,function(b){(D(b)?b.test(a):G(b)?b[a]===f:a===s(b))&&(d=!0)},1);d===c&&(e[a]=f)});return e}H(m,!1,!0,{watch:function(a,b,c){if(ea){var d=a[b];m.defineProperty(a,b,{enumerable:!0,configurable:!0,get:function(){return d},set:function(e){d=c.call(a,b,d,e)}})}}});
H(m,!1,function(){return 1<arguments.length},{keys:function(a,b){var c=m.keys(a);c.forEach(function(c){b.call(a,c,a[c])});return c}});
H(m,!1,!0,{isObject:function(a){return va(a)},isNaN:function(a){return y(a)&&a.valueOf()!==a.valueOf()},equal:function(a,b){return Ua(a,b)},extended:function(a){return new O(a)},merge:function(a,b,c,d){var e,g,f,h,l,n,x;if(a&&"string"!==typeof b)for(e in b)if(J(b,e)&&a){h=b[e];l=a[e];n=M(l);g=G(h);f=G(l);x=n&&!1===d?l:h;n&&F(d)&&(x=d.call(b,e,l,h));if(c&&(g||f))if(C(h))x=new r(h.getTime());else if(D(h))x=new q(h.source,Qa(h));else{f||(a[e]=p.isArray(h)?[]:{});m.merge(a[e],h,c,d);continue}a[e]=x}return a},
values:function(a,b){var c=[];I(a,function(d,e){c.push(e);b&&b.call(a,e)});return c},clone:function(a,b){var c;if(!G(a))return a;c=v.call(a);if(C(a,c)&&a.clone)return a.clone();if(C(a,c)||D(a,c))return new a.constructor(a);if(a instanceof O)c=new O;else if(A(a,c))c=[];else if(va(a,c))c={};else throw new TypeError("Clone must be a basic data type.");return m.merge(c,a,b)},fromQueryString:function(a,b){var c=m.extended();a=a&&a.toString?a.toString():"";a.replace(/^.*?\?/,"").split("&").forEach(function(a){a=
a.split("=");2===a.length&&Ec(c,a[0],decodeURIComponent(a[1]),b)});return c},toQueryString:function(a,b){return Fc(b,a)},tap:function(a,b){var c=b;F(b)||(c=function(){if(b)a[b]()});c.call(a,a);return a},has:function(a,b){return J(a,b)},select:function(a){return Hc(a,arguments,!0)},reject:function(a){return Hc(a,arguments,!1)}});K(m,!1,!0,w,function(a,b){var c="is"+b;Cc.push(c);a[c]=ia[b]});
H(m,!1,function(){return 0===arguments.length},{extend:function(){var a=Cc.concat(Dc);"undefined"!==typeof Hb&&(a=a.concat(Hb));Ya(a,m)}});Ya(Dc,O);
"use strict";H(q,!1,!0,{escape:function(a){return Ra(a)}});H(q,!0,!0,{getFlags:function(){return Qa(this)},setFlags:function(a){return q(this.source,a)},addFlag:function(a){return this.setFlags(Qa(this,a))},removeFlag:function(a){return this.setFlags(Qa(this).replace(a,""))}});
"use strict";
function Ic(a){a=+a;if(0>a||Infinity===a)throw new RangeError("Invalid number");return a}function Jc(a,b){return Na(M(b)?b:" ",a)}function Kc(a,b,c,d,e){var g;if(a.length<=b)return a.toString();d=N(d)?"...":d;switch(c){case "left":return a=e?Lc(a,b,!0):a.slice(a.length-b),d+a;case "middle":return c=Aa(b/2),g=Q(b/2),b=e?Lc(a,c):a.slice(0,c),a=e?Lc(a,g,!0):a.slice(a.length-g),b+d+a;default:return b=e?Lc(a,b):a.slice(0,b),b+d}}
function Lc(a,b,c){if(c)return Lc(a.reverse(),b).reverse();c=q("(?=["+Ma()+"])");var d=0;return a.split(c).filter(function(a){d+=a.length;return d<=b}).join("")}function Mc(a,b,c){z(b)&&(b=a.indexOf(b),-1===b&&(b=c?a.length:0));return b}var Nc,Oc;H(s,!0,!1,{repeat:function(a){a=Ic(a);return Na(this,a)}});
H(s,!0,function(a){return D(a)||2<arguments.length},{startsWith:function(a){var b=arguments,c=b[1],b=b[2],d=this;c&&(d=d.slice(c));N(b)&&(b=!0);c=D(a)?a.source.replace("^",""):Ra(a);return q("^"+c,b?"":"i").test(d)},endsWith:function(a){var b=arguments,c=b[1],b=b[2],d=this;M(c)&&(d=d.slice(0,c));N(b)&&(b=!0);c=D(a)?a.source.replace("$",""):Ra(a);return q(c+"$",b?"":"i").test(d)}});
H(s,!0,!0,{escapeRegExp:function(){return Ra(this)},escapeURL:function(a){return a?encodeURIComponent(this):encodeURI(this)},unescapeURL:function(a){return a?decodeURI(this):decodeURIComponent(this)},escapeHTML:function(){return this.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&apos;").replace(/\//g,"&#x2f;")},unescapeHTML:function(){return this.replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&quot;/g,'"').replace(/&apos;/g,"'").replace(/&#x2f;/g,
"/").replace(/&amp;/g,"&")},encodeBase64:function(){return Nc(unescape(encodeURIComponent(this)))},decodeBase64:function(){return decodeURIComponent(escape(Oc(this)))},each:function(a,b){var c,d,e;F(a)?(b=a,a=/[\s\S]/g):a?z(a)?a=q(Ra(a),"gi"):D(a)&&(a=q(a.source,Qa(a,"g"))):a=/[\s\S]/g;c=this.match(a)||[];if(b)for(d=0,e=c.length;d<e;d++)c[d]=b.call(this,c[d],d,c)||c[d];return c},shift:function(a){var b="";a=a||0;this.codes(function(c){b+=s.fromCharCode(c+a)});return b},codes:function(a){var b=[],
c,d;c=0;for(d=this.length;c<d;c++){var e=this.charCodeAt(c);b.push(e);a&&a.call(this,e,c)}return b},chars:function(a){return this.each(a)},words:function(a){return this.trim().each(/\S+/g,a)},lines:function(a){return this.trim().each(/^.*$/gm,a)},paragraphs:function(a){var b=this.trim().split(/[\r\n]{2,}/);return b=b.map(function(b){if(a)var d=a.call(b);return d?d:b})},isBlank:function(){return 0===this.trim().length},has:function(a){return-1!==this.search(D(a)?a:Ra(a))},add:function(a,b){b=N(b)?
this.length:b;return this.slice(0,b)+a+this.slice(b)},remove:function(a){return this.replace(a,"")},reverse:function(){return this.split("").reverse().join("")},compact:function(){return this.trim().replace(/([\r\n\s\u3000])+/g,function(a,b){return"\u3000"===b?b:" "})},at:function(){return Wa(this,arguments,!0)},from:function(a){return this.slice(Mc(this,a,!0))},to:function(a){N(a)&&(a=this.length);return this.slice(0,Mc(this,a))},dasherize:function(){return this.underscore().replace(/_/g,"-")},underscore:function(){return this.replace(/[-\s]+/g,
"_").replace(s.Inflector&&s.Inflector.acronymRegExp,function(a,b){return(0<b?"_":"")+a.toLowerCase()}).replace(/([A-Z\d]+)([A-Z][a-z])/g,"$1_$2").replace(/([a-z\d])([A-Z])/g,"$1_$2").toLowerCase()},camelize:function(a){return this.underscore().replace(/(^|_)([^_]+)/g,function(b,c,d,e){b=(b=s.Inflector)&&b.acronyms[d];b=z(b)?b:void 0;e=!1!==a||0<e;return b?e?b:b.toLowerCase():e?d.capitalize():d})},spacify:function(){return this.underscore().replace(/_/g," ")},stripTags:function(){var a=this;sa(0<arguments.length?
arguments:[""],function(b){a=a.replace(q("</?"+Ra(b)+"[^<>]*>","gi"),"")});return a},removeTags:function(){var a=this;sa(0<arguments.length?arguments:["\\S+"],function(b){b=q("<("+b+")[^<>]*(?:\\/>|>.*?<\\/\\1>)","gi");a=a.replace(b,"")});return a},truncate:function(a,b,c){return Kc(this,a,b,c)},truncateOnWord:function(a,b,c){return Kc(this,a,b,c,!0)},pad:function(a,b){var c,d;a=Ic(a);c=S(0,a-this.length)/2;d=Q(c);c=Aa(c);return Jc(d,b)+this+Jc(c,b)},padLeft:function(a,b){a=Ic(a);return Jc(S(0,a-
this.length),b)+this},padRight:function(a,b){a=Ic(a);return this+Jc(S(0,a-this.length),b)},first:function(a){N(a)&&(a=1);return this.substr(0,a)},last:function(a){N(a)&&(a=1);return this.substr(0>this.length-a?0:this.length-a)},toNumber:function(a){return Oa(this,a)},capitalize:function(a){var b;return this.toLowerCase().replace(a?/[^']/g:/^\S/,function(a){var d=a.toUpperCase(),e;e=b?a:d;b=d!==a;return e})},assign:function(){var a={};sa(arguments,function(b,c){G(b)?xa(a,b):a[c+1]=b});return this.replace(/\{([^{]+?)\}/g,
function(b,c){return J(a,c)?a[c]:b})}});H(s,!0,!0,{insert:s.prototype.add});
(function(a){if(ba.btoa)Nc=ba.btoa,Oc=ba.atob;else{var b=/[^A-Za-z0-9\+\/\=]/g;Nc=function(b){var d="",e,g,f,h,l,n,x=0;do e=b.charCodeAt(x++),g=b.charCodeAt(x++),f=b.charCodeAt(x++),h=e>>2,e=(e&3)<<4|g>>4,l=(g&15)<<2|f>>6,n=f&63,isNaN(g)?l=n=64:isNaN(f)&&(n=64),d=d+a.charAt(h)+a.charAt(e)+a.charAt(l)+a.charAt(n);while(x<b.length);return d};Oc=function(c){var d="",e,g,f,h,l,n=0;if(c.match(b))throw Error("String contains invalid base64 characters");c=c.replace(/[^A-Za-z0-9\+\/\=]/g,"");do e=a.indexOf(c.charAt(n++)),
g=a.indexOf(c.charAt(n++)),h=a.indexOf(c.charAt(n++)),l=a.indexOf(c.charAt(n++)),e=e<<2|g>>4,g=(g&15)<<4|h>>2,f=(h&3)<<6|l,d+=s.fromCharCode(e),64!=h&&(d+=s.fromCharCode(g)),64!=l&&(d+=s.fromCharCode(f));while(n<c.length);return d}}})("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=");})();
$(() => {
	d20.journal.charsheetFetchPromise.then(() => {
		window.currentPlayer = {
			id: -1,
		};

		let lastName = '';
		let linesSinceName = 0;

		/**
		 * Replaces auto-link generated anchor tags of image urls with image tags in message content.
		 * */
		const swapImageUrlsForHtml = (messageHtml) => {
			const autoLinkRegex = /((<a href='(https?):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|]).(?:jpg|jpeg|gif|png|webp).*(<\/a>))/ig;
			const imageUrlRegex = /(\b(https?):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|]).(?:jpg|jpeg|gif|png|webp)/ig;
			const newContent = messageHtml.replace(
				autoLinkRegex,
				(match, src) => {
					const imgUrl = src.match(imageUrlRegex)[0];
					return `<img src="${imgUrl}" draggable="false"/>`;
				},
			);
			return newContent;
		};

		const incoming = function (op) {
			let template_name = op.type;

			if (op.messageId) {
				d20.textchat.rollHistory[op.messageId] = {
					rolls: op.rolls || {},
					postId: op.id
				}
			}

			// op.content = strip_tags("", op.content);

			if (op.type == 'gmrollresult') {
				if (window.NOGMROLLRESULTS == true) {
					return '';
				}
				if (!window.is_gm && op.playerid != window.currentPlayer.id) {
					return '';
				}
				template_name = 'rollresult';
			}

			if (op.type == 'whisper') {
				if (window.NOWHISPERS == true) {
					return '';
				}

				if (op.playerid == window.currentPlayer.id) {
					template_name = 'whispersent';
				} else {
					template_name = 'whisperreceived';
					if (op.target == 'gm') {
						if (!window.is_gm) {
							return '';
						}
					} else if (op.target != window.currentPlayer.id) {
						return '';
					}

					lastWhisperReceived = op;
				}
			}

			if (template_name == 'rollresult' && op.origRoll) {
				template_name = 'newroll';
				op.htmlcontent = d20.dice_formatter.getHtmlForResult(JSON.parse(op.content));
				op.sanitizedOrigRoll = d20.dice_formatter.replaceInlineRolls(op.origRoll, op);
			} else if (template_name == 'rollresult' && typeof op.content === 'object') {
				// There was about a 3-week period on dev where this was active. whoops.
				op.content = `${op.content.origformula}|${op.content.formula}|${op.content.total}`;
			}

			if (!op.rolltemplate && template_name != 'rollresult' && template_name != 'newroll' && template_name != 'tokenroll' && template_name != 'direct') {
				// op.content = (op.content + "").autoLink();
				op.content = Markdown.parse(`${op.content}`).autoLink();
				op.content = swapImageUrlsForHtml(op.content);
			}

			if (op.type === 'advancedroll') {
				if (op.whisper === 'gm' && !window.is_gm) {
					if (op.playerid !== window.currentPlayer.id || op.secret) {
						return;
					}
				}
				op.content = d20.textchat.displayAdvancedSheetRoll(op);
				op.content = d20.utils.htmlTranslator(op.content, true);
			}

			const template = $(`#tmpl_chatmessage_${template_name}`);

			if (op.who !== lastName || linesSinceName > 5) {
				op.showname = true;
				linesSinceName = 0;
			}

			if (op.rolltemplate) {
				let templateview = {};

				templateview = d20.textchat.buildRollTemplateViewObj(templateview, op);
				templateview = d20.textchat.handleTemplateViewTranslations(templateview);
				templateview = d20.textchat.buildRollTemplateViewFunctions(templateview, op);

				op.content = Mustache.render(d20.textchat.buildRollTemplateHtml(op), templateview);
				op.content = Markdown.parse(op.content);
				op.content = d20.utils.htmlTranslator(op.content, true);
			}

			let translated = template.jqote(op);

			// Replace img element with video if needed
			if (template_name === 'tokenroll') {
				const regex = /<img\s.*src=\"(.*[\w\-]+\.webm(?:\?\d*)?)\"[^>]*>/i;
				translated = translated.replace(
					regex,
					(match, src) => `<video src="${src.replace('/med.webm', '/thumb.webm')}" draggable="false" style="width: 30px; height: 30px;" muted autoplay loop />`,
				);
			}

			if (op.type == 'emote' || op.type == 'gmrollresult' || op.type == 'whisper') {
				lastName = '';
			} else {
				lastName = op.who;
			}
			linesSinceName++;

			return translated;
		};

		const showMessages = function () {
			const totalcount = 0;
			let allhtml = '';
			let allmessages = [];
			let prioritysorted = [];

			const decoded = BASE64.decode(msgdata);

			const rawmessages = JSON.parse(decoded);

			for (var i = 0; i < rawmessages.length; i++) {
				for (const j in rawmessages[i]) {
					rawmessages[i][j].timestamp = rawmessages[i][j]['.priority'];
					if (!rawmessages[i][j].timestamp) {
						rawmessages[i][j].timestamp = '';
					} else {
						const time = rawmessages[i][j].timestamp;
						const d = Date.create(time);
						const now = new Date().getTime();
						if (now - time < 60 * 60 * 24 * 1000) {
							rawmessages[i][j].timestamp = d.format('{h}:{mm}{TT}');
						} else {
							rawmessages[i][j].timestamp = d.format('{{Month}} {{dd}}, {{yyyy}} {h}:{mm}{TT}');
						}
					}
					rawmessages[i][j].id = j;
					// allhtml += incoming(rawmessages[i][j]);
					if (rawmessages[i][j]['.priority'] !== undefined) {
						prioritysorted.push(rawmessages[i][j]);
					} else {
						allmessages.push(rawmessages[i][j]);
					}
				}
			}

			// for(var j in rawmessages[rawmessages.length-1]) {
			// 	(rawmessages[rawmessages.length-1][j]);
			// }

			allmessages = _.sortBy(allmessages, (msg) => msg.id);

			prioritysorted = _.sortBy(prioritysorted, (msg) => msg['.priority']);

			for (var i = 0; i < allmessages.length; i++) {
				try {
					allhtml += incoming(allmessages[i]);
				} catch (e) {
					console.log(`ERROR with message ${allmessages[i].id}`);
					console.log(e);
				}
			}

			// Priorty sorted always come after those without priorities.

			for (var i = 0; i < prioritysorted.length; i++) {
				try {
					allhtml += incoming(prioritysorted[i]);
				} catch (e) {
					console.log(`ERROR with message ${prioritysorted[i].id}`);
					console.log(e);
				}
			}

			$('#textchat .content').html(allhtml);
			$('#textchat .content').find('button[data-sheet-action]').prop('disabled', true);

			function autoGrav() {
				if ($(this).hasClass('tipsy-w')) return 'w';
				if ($(this).hasClass('tipsy-e')) return 'e';
				if ($(this).hasClass('tipsy-n')) return 'n';
				if ($(this).hasClass('tipsy-s')) return 's';
				if ($(this).hasClass('tipsy-n-right')) {
					const rightOffset = $(window).width() - $(this).offset().left;
					return rightOffset < $(this).parents('.message').width() / 2 ? 'ne' : 'n';
				}
				if ($(this).hasClass('tipsy-side')) return $(this).offset().left > ($(document).scrollLeft() + $(window).width() / 2) ? 'e' : 'w';
				return $(this).offset().top > ($(document).scrollTop() + $(window).height() / 2) ? 's' : 'n';
			}

			$('.showtip').tipsy({
				live: true, gravity: autoGrav, opacity: 1.0, html: true,
			});
		};

		showMessages();
	});
});

// tipsy, facebook style tooltips for jquery
// version 1.0.0a
// (c) 2008-2010 jason frame [jason@onehackoranother.com]
// released under the MIT license

(function($) {
    
    function Tipsy(element, options) {
        this.$element = $(element);
        this.options = options;
        this.enabled = true;
        this.fixTitle();
    }
    
    Tipsy.prototype = {
        show: function() {
            var title = this.getTitle();
            if(title == "noshow") {
                return;
            }
            if (title && this.enabled) {
                var $tip = this.tip();

                var container = $("body");

                var offset_top = 0;
                var offset_left = 0;

                if(this.$element.parents("#editor-wrapper").length > 0) {
                    container = $("#editor-wrapper");
                    offset_top = container.scrollTop();
                    offset_left = container.scrollLeft();
                }

                var parentBody = this.$element.parents("body");

                if(parentBody.hasClass("popoutwindow")) {
                    container = parentBody;
                }

                if(this.options.filterhtml) {
                    title = d20ext.utils.strip_tags(title, "<span><br><strong><em>");
                }
                
                $tip.find('.tipsy-inner')[this.options.html ? 'html' : 'text'](title);
                $tip[0].className = 'tipsy'; // reset classname in case of dynamic gravity
                $tip.remove().css({top: 0, left: 0, visibility: 'hidden', display: 'block'}).appendTo(container);


                
                var pos = $.extend({}, this.$element.offset(), {
                    width: this.$element[0].offsetWidth,
                    height: this.$element[0].offsetHeight
                });

                pos.top = pos.top + offset_top;
                pos.left = pos.left + offset_left;
                
                var actualWidth = $tip[0].offsetWidth, actualHeight = $tip[0].offsetHeight;
                var gravity = (typeof this.options.gravity == 'function')
                                ? this.options.gravity.call(this.$element[0])
                                : this.options.gravity;
                
                var tp;
                switch (gravity.charAt(0)) {
                    case 'n':
                        tp = {top: pos.top + pos.height + this.options.offset, left: pos.left + pos.width / 2 - actualWidth / 2};
                        break;
                    case 's':
                        tp = {top: pos.top - actualHeight - this.options.offset, left: pos.left + pos.width / 2 - actualWidth / 2};
                        break;
                    case 'e':
                        tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth - this.options.offset};
                        break;
                    case 'w':
                        tp = {top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width + this.options.offset};
                        break;
                }
                
                if (gravity.length == 2) {
                    if (gravity.charAt(1) == 'w') {
                        tp.left = pos.left + pos.width / 2 - 15;
                    } else {
                        tp.left = pos.left + pos.width / 2 - actualWidth + 15;
                    }
                }
                
                $tip.css(tp).addClass('tipsy-' + gravity);
                
                if (this.options.fade) {
                    $tip.stop().css({opacity: 0, display: 'block', visibility: 'visible'}).animate({opacity: this.options.opacity});
                } else {
                    $tip.css({visibility: 'visible', opacity: this.options.opacity});
                }
                $tip.on("mousedown", ".noshow", function() {
                    var tutname = $(this).attr("data-tutorial");
                    window.ignore_tutorials.push(tutname);
                    $(".tipsy").remove();
                    $.post("/editor/disable_tutorial/" + tutname);
                    return false;
                });
            }
        },
        
        hide: function() {
            if (this.options.fade) {
                this.tip().stop().fadeOut(function() { $(this).remove(); });
            } else {
                this.tip().remove();
            }
        },
        
        fixTitle: function() {
            var $e = this.$element;
            if ($e.attr('title') || typeof($e.attr('original-title')) != 'string') {
                $e.attr('original-title', $e.attr('title') || '').removeAttr('title');
            }
        },
        
        getTitle: function() {
            var title, $e = this.$element, o = this.options;
            this.fixTitle();
            var title, o = this.options;
            if (typeof o.title == 'string') {
                title = $e.attr(o.title == 'title' ? 'original-title' : o.title);
            } else if (typeof o.title == 'function') {
                title = o.title.call($e[0]);
            }
            title = ('' + title).replace(/(^\s*|\s*$)/, "");
            return title || o.fallback;
        },
        
        tip: function() {
            if (!this.$tip) {
                if(this.options.userscript) {
                    this.$tip = $('<div class="tipsy"></div>').html('<div class="tipsy-arrow"></div><div class="tipsy-inner userscript-tipsy-inner"></div><div class="tipsy-userscript-warning">API or player-generated content</div>');
                }
                else {
                    this.$tip = $('<div class="tipsy"></div>').html('<div class="tipsy-arrow"></div><div class="tipsy-inner"></div>');
                }
            }
            return this.$tip;
        },
        
        validate: function() {
            if (!this.$element[0].parentNode) {
                this.hide();
                this.$element = null;
                this.options = null;
            }
        },
        
        enable: function() { this.enabled = true; },
        disable: function() { this.enabled = false; },
        toggleEnabled: function() { this.enabled = !this.enabled; }
    };
    
    $.fn.tipsy = function(options) {
        
        if (options === true) {
            return this.data('tipsy');
        } else if (typeof options == 'string') {
            var tipsy = this.data('tipsy');
            if (tipsy) tipsy[options]();
            return this;
        }
        
        options = $.extend({}, $.fn.tipsy.defaults, options);
        
        function get(ele) {
            var tipsy = $.data(ele, 'tipsy');
            if (!tipsy) {
                tipsy = new Tipsy(ele, $.fn.tipsy.elementOptions(ele, options));
                $.data(ele, 'tipsy', tipsy);
            }
            return tipsy;
        }
        
        function enter() {
            var tipsy = get(this);
            tipsy.hoverState = 'in';
            if (options.delayIn == 0) {
                tipsy.show();
            } else {
                tipsy.fixTitle();
                setTimeout(function() { if (tipsy.hoverState == 'in') tipsy.show(); }, options.delayIn);
            }
        };
        
        function leave() {
            var tipsy = get(this);
            tipsy.hoverState = 'out';
            if (options.delayOut == 0) {
                tipsy.hide();
            } else {
                setTimeout(function() { if (tipsy.hoverState == 'out') tipsy.hide(); }, options.delayOut);
            }
        };
        
        if (!options.live) this.each(function() { get(this); });
        
        if (options.trigger != 'manual') {
            var eventIn = options.trigger == 'hover' ? 'mouseenter' : 'focus',
                eventOut = options.trigger == 'hover' ? 'mouseleave' : 'blur';
            if (options.live)
                $(document).on(eventIn, this.selector, enter).on(eventOut, this.selector, leave);
            else
                this.bind(eventIn, enter).bind(eventOut, leave);
        }
        
        return this;
        
    };
    
    $.fn.tipsy.defaults = {
        delayIn: 0,
        delayOut: 0,
        fade: false,
        fallback: '',
        gravity: 'n',
        html: false,
        live: false,
        offset: 0,
        opacity: 0.9,
        title: 'title',
        trigger: 'hover',
        conatinerel: false
    };
    
    // Overwrite this method to provide options on a per-element basis.
    // For example, you could store the gravity in a 'tipsy-gravity' attribute:
    // return $.extend({}, options, {gravity: $(ele).attr('tipsy-gravity') || 'n' });
    // (remember - do not modify 'options' in place!)
    $.fn.tipsy.elementOptions = function(ele, options) {
        return $.metadata ? $.extend({}, options, $(ele).metadata()) : options;
    };
    
    $.fn.tipsy.autoNS = function() {
        return $(this).offset().top > ($(document).scrollTop() + $(window).height() / 2) ? 's' : 'n';
    };
    
    $.fn.tipsy.autoWE = function() {
        return $(this).offset().left > ($(document).scrollLeft() + $(window).width() / 2) ? 'e' : 'w';
    };
    
})(jQuery);

/*
jQuery Redirect v1.1.3

Copyright (c) 2013-2018 Miguel Galante
Copyright (c) 2011-2013 Nemanja Avramovic, www.avramovic.info

Licensed under CC BY-SA 4.0 License: http://creativecommons.org/licenses/by-sa/4.0/

This means everyone is allowed to:

Share - copy and redistribute the material in any medium or format
Adapt - remix, transform, and build upon the material for any purpose, even commercially.
Under following conditions:

Attribution - You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
ShareAlike - If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
*/
;(function ($) {
  'use strict';

  //Defaults configuration
  var defaults = {
    url: null,
    values: null,
    method: "POST",
    target: null,
    traditional: false,
    redirectTop: false
  };

  /**
  * jQuery Redirect
  * @param {string} url - Url of the redirection
  * @param {Object} values - (optional) An object with the data to send. If not present will look for values as QueryString in the target url.
  * @param {string} method - (optional) The HTTP verb can be GET or POST (defaults to POST)
  * @param {string} target - (optional) The target of the form. "_blank" will open the url in a new window.
  * @param {boolean} traditional - (optional) This provides the same function as jquery's ajax function. The brackets are omitted on the field name if its an array.  This allows arrays to work with MVC.net among others.
  * @param {boolean} redirectTop - (optional) If its called from a iframe, force to navigate the top window. 
  *//**
  * jQuery Redirect
  * @param {string} opts - Options object
  * @param {string} opts.url - Url of the redirection
  * @param {Object} opts.values - (optional) An object with the data to send. If not present will look for values as QueryString in the target url.
  * @param {string} opts.method - (optional) The HTTP verb can be GET or POST (defaults to POST)
  * @param {string} opts.target - (optional) The target of the form. "_blank" will open the url in a new window.
  * @param {boolean} opts.traditional - (optional) This provides the same function as jquery's ajax function. The brackets are omitted on the field name if its an array.  This allows arrays to work with MVC.net among others.
  * @param {boolean} opts.redirectTop - (optional) If its called from a iframe, force to navigate the top window. 
  */
  $.redirect = function (url, values, method, target, traditional, redirectTop) {
    var opts = url;
    if (typeof url !== "object") {
      var opts = {
        url: url,
        values: values,
        method: method,
        target: target,
        traditional: traditional,
        redirectTop: redirectTop
      };
    }

    var config = $.extend({}, defaults, opts);
    var generatedForm = $.redirect.getForm(config.url, config.values, config.method, config.target, config.traditional);
    $('body', config.redirectTop ? window.top.document : undefined).append(generatedForm.form);
    generatedForm.submit();
    generatedForm.form.remove();
  };

  $.redirect.getForm = function (url, values, method, target, traditional) {
    method = (method && ["GET", "POST", "PUT", "DELETE"].indexOf(method.toUpperCase()) !== -1) ? method.toUpperCase() : 'POST';

    url = url.split("#");
    var hash = url[1] ? ("#" + url[1]) : "";
    url = url[0];

    if (!values) {
      var obj = $.parseUrl(url);
      url = obj.url;
      values = obj.params;
    }

    values = removeNulls(values);

    var form = $('<form>')
      .attr("method", method)
      .attr("action", url + hash);


    if (target) {
      form.attr("target", target);
    }

    var submit = form[0].submit;
    iterateValues(values, [], form, null, traditional);

    return { form: form, submit: function () { submit.call(form[0]); } };
  }

  //Utility Functions
	/**
	 * Url and QueryString Parser.
	 * @param {string} url - a Url to parse.
	 * @returns {object} an object with the parsed url with the following structure {url: URL, params:{ KEY: VALUE }}
	 */
  $.parseUrl = function (url) {

    if (url.indexOf('?') === -1) {
      return {
        url: url,
        params: {}
      };
    }
    var parts = url.split('?'),
      query_string = parts[1],
      elems = query_string.split('&');
    url = parts[0];

    var i, pair, obj = {};
    for (i = 0; i < elems.length; i += 1) {
      pair = elems[i].split('=');
      obj[pair[0]] = pair[1];
    }

    return {
      url: url,
      params: obj
    };
  };

  //Private Functions
  var getInput = function (name, value, parent, array, traditional) {
    var parentString;
    if (parent.length > 0) {
      parentString = parent[0];
      var i;
      for (i = 1; i < parent.length; i += 1) {
        parentString += "[" + parent[i] + "]";
      }

      if (array) {
        if (traditional)
          name = parentString;
        else
          name = parentString + "[" + name + "]";
      } else {
        name = parentString + "[" + name + "]";
      }
    }

    return $("<input>").attr("type", "hidden")
      .attr("name", name)
      .attr("value", value);
  };

  var iterateValues = function (values, parent, form, isArray, traditional) {
    var i, iterateParent = [];
    Object.keys(values).forEach(function (i) {
      if (typeof values[i] === "object") {
        iterateParent = parent.slice();
        iterateParent.push(i);
        iterateValues(values[i], iterateParent, form, Array.isArray(values[i]), traditional);
      } else {
        form.append(getInput(i, values[i], parent, isArray, traditional));
      }
    });
  };

  var removeNulls = function (values) {
    var propNames = Object.getOwnPropertyNames(values);
    for (var i = 0; i < propNames.length; i++) {
      var propName = propNames[i];
      if (values[propName] === null || values[propName] === undefined) {
        delete values[propName];
      } else if (typeof values[propName] === 'object') {
        values[propName] = removeNulls(values[propName]);
      } else if (values[propName].length < 1) {
        delete values[propName];
      }
    }
    return values;
  };
}(window.jQuery || window.Zepto || window.jqlite));